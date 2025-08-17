from typing import Any
import uuid
from sqlalchemy import text
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.data_structure import parse_id
from src.lib.tokens.cbc_hmac import (
    HdrT,
    check_cbc_hmac,
    gen_cbc_hmac,
)
from src.lib.tokens.jwe import check_jwe, gen_jwe
from src.lib.tokens.jwt import gen_jwt, verify_jwt
from src.models.token import TokenT
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def handle_user(user_data: RegisterFormT, trx: AsyncSession) -> User:
    stm = """
        SELECT us.*
        FROM users us
        WHERE us.email = :email
        LIMIT 1
        """
    row = (await trx.execute(text(stm), {"email": user_data["email"]})).first()

    if row:
        us = await trx.get(User, row.id)
    else:
        data = {k: v for k, v in user_data.items() if k != "password"}
        user_id = parse_id(uuid.uuid4())
        plain_pwd = user_data["password"]

        us = User(**data, id=user_id)
        await us.set_pwd(plain_pwd)
        trx.add(us)
        await trx.flush([us])
        await trx.refresh(us)

    if not us:
        raise ErrAPI(msg="👻 user disappeared", status=500)

    return us


async def tokens_health_svc(user_data: RegisterFormT) -> Any:
    async with db_trx() as trx:

        us = await handle_user(user_data, trx)
        parsed_us_id: str = parse_id(us.id)

        access_token: str = gen_jwt({"user_id": parsed_us_id})
        result_jwe = await gen_jwe(user_id=parsed_us_id, trx=trx)

        hdr: HdrT = {
            "token_t": TokenT.MANAGE_ACC,
        }

        result_cbc_hmac = await gen_cbc_hmac(
            payload={"user_id": parsed_us_id}, hdr=hdr, trx=trx
        )

        return {
            "new_user": us.to_d(exclude_keys=["password"]),
            "access_token": access_token,
            "access_token_decoded": verify_jwt(
                access_token,
            ),
            "refresh_token": result_jwe["refresh_client"],
            "refresh_token_db": result_jwe["refresh_server"].to_d(),
            "refresh_token_decrypted": await check_jwe(
                result_jwe["refresh_client"]
            ),
            "cbc_hmac_token": result_cbc_hmac["client_token"],
            "cbc_hmac_db": result_cbc_hmac["server_token"].to_d(),
            "cbc_hmac_token_len": len(result_cbc_hmac["client_token"]),
            "cbc_hmac_token_parts_len": list(
                map(len, (result_cbc_hmac["client_token"]).split("."))
            ),
            "cbc_hmac_decrypted": await check_cbc_hmac(
                result_cbc_hmac["client_token"], trx=trx
            ),
        }
