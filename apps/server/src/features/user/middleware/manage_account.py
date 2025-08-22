from fastapi import Request
from src.decorators.err import ErrAPI
from src.lib.hashing.idx import check_pwd
from src.lib.validators.idx import PwdFormT
from src.middleware.check_form import check_form_mdw
from src.middleware.check_jwt import check_jwt_mdw
from src.models.user import UserDcT


class ManageAccountForm(PwdFormT):
    pass


async def manage_account_mdw(req: Request) -> UserDcT:
    us: UserDcT = await check_jwt_mdw(req)

    result = await check_form_mdw(ManageAccountForm, req)

    if not (await check_pwd(hashed=us["password"], plain=result.password)):
        raise ErrAPI(msg="invalid password", status=401)

    return us
