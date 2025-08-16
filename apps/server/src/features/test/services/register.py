import json
from typing import Any, cast
import uuid
from sqlalchemy import select, text
from src.conf.db import db_trx
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.algs.cbc import dec_aes_cbc
from src.lib.algs.hkdf import derive_hkdf_cbc_hmac
from src.lib.algs.hmac import gen_hmac
from src.lib.data_structure import d_to_b, h_to_b, parse_enum, parse_id
from src.lib.etc import lt_now
from src.lib.tokens.cbc_hmac import (
    AadT,
    HdrT,
    constant_time_check,
    gen_cbc_hmac,
)
from src.lib.tokens.jwe import check_jwe, gen_jwe
from src.lib.tokens.jwt import gen_jwt, verify_jwt
from src.models.token import AlgT, Token, TokenT
from src.models.user import User


async def register_flow_test_ctrl(user_data: RegisterFormT) -> Any:
    async with db_trx() as trx:
        stm = """
        SELECT us.*
        FROM users us
        WHERE us.email = :email
        LIMIT 1
        """
        row = (
            await trx.execute(text(stm), {"email": user_data["email"]})
        ).first()

        if row:
            us = await trx.get(User, row.id)
        else:
            data = {k: v for k, v in user_data.items() if k != "password"}
            user_id = uuid.uuid4()
            plain_pwd = user_data["password"]

            us = User(**data, id=user_id)
            await us.set_pwd(plain_pwd)
            trx.add(us)
            await trx.flush([us])
            await trx.refresh(us)

        if not us:
            raise ErrAPI(msg="👻 user disappeared", status=500)

        access_token: str = gen_jwt({"user_id": parse_id(us.id)})
        result_jwe = await gen_jwe(user_id=parse_id(us.id), trx=trx)

        hdr: HdrT = {
            "alg": AlgT.AES_CBC_HMAC_SHA256,
            "token_t": TokenT.CONF_EMAIL,
        }

        result_cbc_hmac = await gen_cbc_hmac(
            payload={"user_id": parse_id(us.id)}, hdr=hdr, trx=trx
        )

        client_token = result_cbc_hmac["client_token"]

        aad_hex, iv_hex, ct_hex, tag_hex = client_token.split(".")

        aad_d: AadT = json.loads(h_to_b(aad_hex).decode("utf-8"))

        stm = select(Token).where(
            (Token.id == uuid.UUID(aad_d["token_id"]))
            & (Token.token_t == TokenT(aad_d["token_t"]))
        )
        existing = cast(
            Token, (await trx.execute(stm)).scalar_one_or_none()
        ).to_d()

        if lt_now(existing["exp"]):
            raise ErrAPI(msg="token expired", status=401)

        info_b: bytes = d_to_b(
            {
                "alg": parse_enum(existing["alg"]),
                "token_t": parse_enum(existing["token_t"]),
                "user_id": parse_id(existing["user_id"]),
            }
        )

        derived = derive_hkdf_cbc_hmac(
            master=h_to_b(get_env().master_key),
            info=info_b,
            salt=h_to_b(aad_d["salt"]),
        )

        comp_tag = gen_hmac(
            derived["k_1"],
            d_to_b(
                {"aad": aad_hex, "iv": iv_hex, "ciphertext": ct_hex},
            ),
        )

        pt = dec_aes_cbc(
            derived["k_0"], iv=h_to_b(iv_hex), ciphertext=h_to_b(ct_hex)
        )

        if not constant_time_check(h_to_b(tag_hex), comp_tag):
            raise ErrAPI(msg="invalid token", status=401)

        return {
            "new_user": us.to_d(exclude_keys=["password"]),
            "access_token": access_token,
            "access_decoded": verify_jwt(
                access_token,
            ),
            "refresh_token": result_jwe["refresh_client"],
            "refresh_decrypted": await check_jwe(result_jwe["refresh_client"]),
            "client_token": result_cbc_hmac["client_token"],
            "client_token_saved": result_cbc_hmac["server_token"].to_d(),
            "client_token_decrypted": json.loads(pt.decode("utf-8")),
        }
