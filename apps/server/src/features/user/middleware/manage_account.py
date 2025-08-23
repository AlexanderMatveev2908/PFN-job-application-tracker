from fastapi import Request
from src.decorators.err import ErrAPI
from src.lib.hashing.idx import check_pwd
from src.lib.validators.idx import PwdFormT
from src.middleware.check_form import check_form_mdw
from src.middleware.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT


async def manage_account_mdw(req: Request) -> UserDcT:
    us: UserDcT = await check_jwt_search_us_mdw(
        req,
    )

    result = await check_form_mdw(PwdFormT, req)

    if not (await check_pwd(hashed=us["password"], plain=result.password)):
        raise ErrAPI(msg="invalid password", status=401)

    return us
