from typing import TypedDict
import uuid
from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.algs.hmac import hash_db_hmac
from src.lib.data_structure import b_to_h
from src.lib.etc import calc_exp
from src.lib.tokens.jwe import gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import AlgT, Token, TokenT
from src.models.user import User


class RegisterSvcReturnT(TypedDict):
    new_user: dict
    access_token: str
    refresh_token: str


async def register_user_svc(user_data: RegisterFormT) -> RegisterSvcReturnT:
    async with db_trx() as trx:

        stmt = select(User).where(User.email == user_data["email"])
        existing = (await trx.execute(stmt)).scalar_one_or_none()

        if existing:
            raise ErrAPI(msg="user already exists", status=409)

        data = {k: v for k, v in user_data.items() if k != "password"}
        plain_pwd = user_data["password"]

        user_id = uuid.uuid4()
        new_user = User(**data, id=user_id)
        await new_user.set_pwd(plain_pwd)

        access_token: str = gen_jwt(id=str(new_user.id))
        refresh_token: bytes = await gen_jwe(id=str(new_user.id))

        refresh_db = Token(
            user_id=user_id,
            alg=AlgT.RSA_OAEP_256_A256GCM,
            exp=calc_exp("1d"),
            token_t=TokenT.REFRESH,
            hashed=hash_db_hmac(refresh_token),
        )

        trx.add_all([new_user, refresh_db])
        await trx.flush([new_user, refresh_db])
        await trx.refresh(new_user)
        await trx.refresh(refresh_db)

        return {
            "new_user": new_user.to_d(exclude_keys=["password"]),
            "access_token": access_token,
            "refresh_token": b_to_h(refresh_token),
        }
