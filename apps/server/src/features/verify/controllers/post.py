from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.lib.tokens.cbc_hmac import CheckCbcHmacReturnT
from src.middleware.check_token import check_cbc_hmac_mdw


def confirm_email_ctrl(
    _: Request, cbc_result: CheckCbcHmacReturnT = Depends(check_cbc_hmac_mdw)
) -> ResAPI:

    return ResAPI.ok_200(**cbc_result)
