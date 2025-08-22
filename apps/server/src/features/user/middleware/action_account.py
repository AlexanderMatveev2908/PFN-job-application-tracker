from fastapi import Request

from src.lib.tokens.jwt import check_jwt
from src.middleware.check_jwt import extract_jwt
from src.models.token import PayloadT


async def action_account_mdw(req: Request) -> None:
    decoded: PayloadT = check_jwt(extract_jwt(req))
