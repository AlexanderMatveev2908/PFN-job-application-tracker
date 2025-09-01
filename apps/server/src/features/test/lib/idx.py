from typing import cast
from fastapi import Request
from src.__dev_only.payloads import (
    PayloadRegisterPartT,
    RegisterPayloadT,
    get_payload_register,
)
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.data_structure import pick
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


async def get_optional_payload(req: Request) -> PayloadRegisterPartT:
    body: RegisterPayloadT | None = None
    try:
        body = await req.json()
    except Exception:
        ...

    if body:
        try:
            RegisterFormT(**cast(RegisterFormT, body))
        except Exception:
            raise ErrAPI(msg="invalid payload 😡", status=400)

    payload = body or get_payload_register()
    filtered = pick(payload, keys_off=["confirm_password"])

    return cast(PayloadRegisterPartT, filtered)
