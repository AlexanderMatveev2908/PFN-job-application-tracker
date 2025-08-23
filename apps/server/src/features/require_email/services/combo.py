from src.conf.env import get_env
from src.lib.emails.aiosmtp.idx import send_email
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.models.token import TokenT
from src.models.user import UserDcT
from sqlalchemy.ext.asyncio import AsyncSession

can_send = get_env().py_env != "test"


mapper_subj = {
    TokenT.RECOVER_PWD: "RECOVER ACCOUNT 🔒",
    TokenT.CHANGE_EMAIL: "CHANGE EMAIL ADDRESS 📮",
    TokenT.CONF_EMAIL: "CONFIRM EMAIL ADDRESS 🛡️",
}


async def gen_token_send_email_svc(
    trx: AsyncSession,
    us_d: UserDcT,
    token_t: TokenT,
    callback_url: str = "",
    email_to: str | None = None,
) -> None:

    cbc_hmac_result = await gen_cbc_hmac(
        user_id=us_d["id"], trx=trx, token_t=token_t
    )

    if can_send:
        await send_email(
            callback_url=callback_url
            or f"https://pfn-job-application-tracker-client.fly.dev?cbc_hmac_token={cbc_hmac_result['client_token']}",  # noqa: E501
            subj=mapper_subj[token_t],
            user=us_d,
            email_to=email_to,
        )
