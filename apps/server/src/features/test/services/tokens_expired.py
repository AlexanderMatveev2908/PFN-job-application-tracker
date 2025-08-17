from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.features.test.lib.register_user import handle_user_lib
from src.lib.data_structure import parse_id
from src.lib.tokens.cbc_hmac import CbcHmacReturnT, gen_cbc_hmac
from src.lib.tokens.jwe import JweReturnT, gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import TokenT


async def tokens_expired_svc(user_data: RegisterFormT) -> dict:
    async with db_trx() as trx:
        us = await handle_user_lib(user_data, trx)

        parsed_us_id: str = parse_id(us.id)

        access_token: str = gen_jwt({"user_id": parsed_us_id}, reverse=True)
        result_jwe: JweReturnT = await gen_jwe(
            user_id=parsed_us_id, trx=trx, reverse=True
        )

        result_cbc_hmac: CbcHmacReturnT = await gen_cbc_hmac(
            payload={"user_id": parsed_us_id},
            hdr={
                "token_t": TokenT.MANAGE_ACC,
            },
            trx=trx,
            reverse=False,
        )

        return {
            "access_token": access_token,
            "refresh_token": result_jwe["client_token"],
            "cbc_hmac": result_cbc_hmac["client_token"],
        }
