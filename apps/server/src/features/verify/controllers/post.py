from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.middleware.check_token import check_cbc_hmac_mdw
from src.models.token import CheckTokenReturnT


def confirm_email_ctrl(
    _: Request, cbc_result: CheckTokenReturnT = Depends(check_cbc_hmac_mdw)
) -> ResAPI:

    return ResAPI.ok_200(**cbc_result)
