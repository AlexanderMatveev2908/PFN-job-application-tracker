from fastapi import Request
from src.decorators.err import ErrAPI
from src.models.token import TokenT


def get_query_token_t(req: Request) -> TokenT:

    token_t = req.query_params.get("cbc_hmac_token_t")

    if not token_t:
        raise ErrAPI(msg="token type not provided", status=400)

    try:
        parsed = TokenT(token_t)
        return parsed
    except Exception:
        raise ErrAPI(msg="invalid token type", status=400)
