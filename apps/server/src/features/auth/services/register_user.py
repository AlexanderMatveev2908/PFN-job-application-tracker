from typing import TypedDict
import uuid
from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.data_structure import parse_id
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.jwe import gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import User


class RegisterSvcReturnT(TypedDict):
    new_user: dict
    access_token: str
    refresh_token: str
    cbc_hmac_token: str


async def register_user_svc(user_data: RegisterFormT) -> RegisterSvcReturnT:
    async with db_trx() as trx:

        stmt = select(User).where(User.email == user_data["email"])
        existing = (await trx.execute(stmt)).scalar_one_or_none()

        if existing:
            raise ErrAPI(msg="user already exists", status=409)

        data = {k: v for k, v in user_data.items() if k != "password"}
        plain_pwd = user_data["password"]

        user_id = parse_id(uuid.uuid4())
        new_user = User(**data, id=user_id)
        await new_user.set_pwd(plain_pwd)

        trx.add(new_user)
        await trx.flush([new_user])
        await trx.refresh(new_user)

        access_token: str = gen_jwt({"user_id": user_id})
        result_jwe: GenTokenReturnT = await gen_jwe(user_id=user_id, trx=trx)

        cbc_hmac_res: GenTokenReturnT = await gen_cbc_hmac(
            hdr={
                "token_t": TokenT.REFRESH,
            },
            payload={"user_id": user_id},
            trx=trx,
        )

        return {
            "new_user": new_user.to_d(exclude_keys=["password"]),
            "access_token": access_token,
            "refresh_token": result_jwe["client_token"],
            "cbc_hmac_token": cbc_hmac_res["client_token"],
        }
