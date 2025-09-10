from typing import cast
from fastapi import Request, Response
from sqlalchemy import delete

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.data_structure.parsers import b_to_d, h_to_b
from src.lib.tokens.cbc_hmac import AadT
from src.models.token import Token


async def clean_cbc_hmac_ctrl(
    req: Request,
) -> Response:

    token_id: str = ""

    try:
        cbc_hmac_token = req.query_params.get("cbc_hmac-token", "")
        aad_hex, *_ = cbc_hmac_token.split(".")

        token_id = cast(
            AadT,
            b_to_d(
                h_to_b(aad_hex),
            ),
        )["token_id"]
    except Exception:
        ...

    if not token_id:
        raise ErrAPI(msg="cbc_hmac_invalid", status=400)

    async with db_trx() as trx:

        result = await trx.execute(delete(Token).where(Token.id == token_id))

        if result.rowcount >= 1:

            return ResAPI(req).ok_204()
        else:
            raise ErrAPI(msg="cbc_hmac_not_found", status=400)
