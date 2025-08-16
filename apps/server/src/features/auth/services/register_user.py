from time import time
from typing import TypedDict
import uuid
from sqlalchemy import select
from src.conf.db import db_trx
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.algs.hmac import gen_hmac
from src.lib.data_structure import b_to_h, h_to_b
from src.lib.tokens.jwe import gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import AlgT, Token, TokenT
from src.models.user import User


class RegisterSvcReturnT(TypedDict):
    new_user: User
    access_token: str
    refresh_token: str


PEPPER_K = get_env().pepper_key


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
            exp=(time() + 1000 * 60**2 * 24),
            token_t=TokenT.REFRESH,
            hashed=gen_hmac(h_to_b(PEPPER_K), refresh_token),
        )

        trx.add_all([new_user, refresh_db])
        await trx.flush([new_user, refresh_db])
        await trx.refresh(new_user)
        await trx.refresh(refresh_db)

        print(refresh_db.to_d())

        return {
            "new_user": new_user,
            "access_token": access_token,
            "refresh_token": b_to_h(refresh_token),
        }
