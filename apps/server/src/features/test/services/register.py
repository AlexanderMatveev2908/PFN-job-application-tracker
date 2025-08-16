from typing import Any
import uuid
from sqlalchemy import text
from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.lib.algs.hmac import hash_db_hmac
from src.lib.data_structure import b_to_h
from src.lib.etc import calc_exp
from src.lib.tokens.jwe import gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import AlgT, Token, TokenT
from src.models.user import User


async def register_flow_test_ctrl(user_data: RegisterFormT) -> Any:

    async with db_trx() as trx:
        stm = """
        SELECT us.*
        FROM users us
        WHERE us.email = :email
        LIMIT 1
        --
        """
        res = (
            await trx.execute(text(stm), {"email": user_data["email"]})
        ).scalar()

        if res:
            us = res.first()

        else:
            data = {k: v for k, v in user_data.items() if k != "password"}
            plain_pwd = user_data["password"]
            user_id = uuid.uuid4()

            us = User(**data, id=user_id)
            await us.set_pwd(plain_pwd)

            access_token: str = gen_jwt(id=str(us.id))
            refresh_token: bytes = await gen_jwe(id=str(us.id))

            refresh_db = Token(
                user_id=user_id,
                alg=AlgT.RSA_OAEP_256_A256GCM,
                exp=calc_exp("1d"),
                token_t=TokenT.REFRESH,
                hashed=hash_db_hmac(refresh_token),
            )

            trx.add_all([us, refresh_db])

            await trx.flush([us, refresh_db])

            await trx.refresh(us)
            await trx.refresh(refresh_db)

            return {
                "new_user": us.to_d(exclude_keys=["password"]),
                "access_token": access_token,
                "refresh_token": b_to_h(refresh_token),
            }
