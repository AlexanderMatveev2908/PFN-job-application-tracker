import uuid
from src.conf.db import db_trx
from src.models.token import AlgT, Token, TokenT


async def gen_token_svc(
    token_id: uuid.UUID,
    user_id: str,
    token_t: TokenT,
    exp: int,
    alg: AlgT,
    hashed: bytes | None = None,
) -> Token:

    async with db_trx() as trx:
        tk = Token(
            id=token_id,
            user_id=user_id,
            token_t=token_t,
            exp=exp,
            hashed=hashed,
            alg=alg,
        )

        trx.add(tk)
        await trx.flush([tk])
        await trx.refresh(tk)

        return tk
