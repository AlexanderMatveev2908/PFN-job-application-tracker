from typing import Any
import uuid
from sqlalchemy import text
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.algs.hmac import hash_db_hmac
from src.lib.data_structure import b_to_h, parse_id
from src.lib.etc import calc_exp
from src.lib.tokens.cbc_hmac import HdrT, gen_cbc_hmac
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
            id=result_cbc_hmac["token_id"],
            user_id=us.id,
            exp=calc_exp("15m"),
            **hdr,
        )

        trx.add(new_cbc_hmac)

        await trx.flush([new_cbc_hmac])
        await trx.refresh(new_cbc_hmac)

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
        }
