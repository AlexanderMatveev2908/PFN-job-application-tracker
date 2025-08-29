from typing import TypedDict
import uuid
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.combo.token_mail import gen_token_send_email_svc
from src.lib.db.idx import get_us_by_email
from src.lib.tokens.combo import gen_tokens_session
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import User


class RegisterSvcReturnT(TypedDict):
    new_user: dict
    access_token: str
    refresh_token: str
    cbc_hmac_token: str


async def register_user_svc(user_data: RegisterFormT) -> RegisterSvcReturnT:
    async with db_trx() as trx:

        existing = await get_us_by_email(
            trx, user_data["email"], must_exists=False
        )

        if existing:
            raise ErrAPI(msg="user already exists", status=409)

        data = {k: v for k, v in user_data.items() if k != "password"}
        plain_pwd = user_data["password"]

        user_id = uuid.uuid4()
        new_user = User(**data, id=user_id)
        await new_user.set_pwd(plain_pwd)

        trx.add(new_user)
        await trx.flush([new_user])
        await trx.refresh(new_user)

        result_tokens = await gen_tokens_session(
            user_id=new_user.id,
            trx=trx,
        )

        cbc_hmac_res: GenTokenReturnT = await gen_token_send_email_svc(
            trx=trx,
            us_d=new_user,
            token_t=TokenT.CONF_EMAIL,
        )

        return {
            "new_user": new_user.to_d(exclude_keys=["password"]),
            "access_token": result_tokens["access_token"],
            "refresh_token": result_tokens["result_jwe"]["client_token"],
            "cbc_hmac_token": cbc_hmac_res["client_token"],
        }
