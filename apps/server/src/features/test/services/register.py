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
from src.lib.algs.hmac import gen_hmac, hash_db_hmac
from src.lib.data_structure import b_to_h, d_to_b, h_to_b, parse_enum, parse_id
from src.lib.etc import calc_exp, lt_now
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
            plain_pwd = user_data["password"]
            user_id = uuid.uuid4()

            us = User(**data, id=user_id)
            await us.set_pwd(plain_pwd)
            trx.add(us)
            await trx.flush([us])
            await trx.refresh(us)

        if not us:
            raise ErrAPI(msg="👻 user disappeared", status=500)

        access_token: str = gen_jwt(id=parse_id(us.id))
        refresh_token: bytes = await gen_jwe(id=parse_id(us.id))

        refresh_db = Token(
            user_id=us.id,
            alg=AlgT.RSA_OAEP_256_A256GCM,
            exp=calc_exp("1d"),
            token_t=TokenT.REFRESH,
            hashed=hash_db_hmac(refresh_token),
        )

        trx.add(refresh_db)
        await trx.flush([refresh_db])
        await trx.refresh(refresh_db)

        hdr: HdrT = {
            "alg": AlgT.AES_CBC_HMAC_SHA256,
            "token_t": TokenT.CONF_EMAIL,
        }

        result_cbc_hmac = gen_cbc_hmac(
            payload={"user_id": parse_id(us.id)}, hdr=hdr
        )

        new_cbc_hmac = Token(
            id=str(result_cbc_hmac["token_id"]),
            user_id=us.id,
            exp=calc_exp("15m"),
            **hdr,
        )
        client_token = result_cbc_hmac["client_token"]

        trx.add(new_cbc_hmac)

        await trx.flush([new_cbc_hmac])
        await trx.refresh(new_cbc_hmac)

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
            "refresh_token": b_to_h(refresh_token),
            "refresh_decrypted": await check_jwe(refresh_token),
            "client_token": result_cbc_hmac["client_token"],
            "client_token_saved": new_cbc_hmac.to_d(),
            "client_token_decrypted": json.loads(pt.decode("utf-8")),
        }
