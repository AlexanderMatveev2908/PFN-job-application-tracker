from src.conf.db import db_trx
from src.conf.env import get_env
from src.lib.emails.aiosmtp.idx import send_email
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.models.token import TokenT
from src.models.user import UserDcT

can_send = get_env().py_env != "test"


async def gen_token_send_email_svc(us_d: UserDcT, token_t: TokenT) -> None:
    async with db_trx() as trx:

        cbc_hmac_result = await gen_cbc_hmac(
            user_id=us_d["id"], trx=trx, token_t=token_t
        )

        if can_send:
            await send_email(
                callback_url=f"https://pfn-job-application-tracker-client.fly.dev?cbc_hmac_token={cbc_hmac_result['client_token']}",  # noqa: E501
                subj="RECOVER PASSWORD 🔒",
                user=us_d,
            )
