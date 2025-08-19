from fastapi import Request
from src.models.token import TokenT


def get_query_token_t(req: Request) -> TokenT:
    return TokenT(req.query_params.get("cbc_hmac_token_t", "CONF_EMAIL"))
