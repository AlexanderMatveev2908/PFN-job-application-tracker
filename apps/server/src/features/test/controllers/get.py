from fastapi import Depends, Request
from src.__dev_only.payloads import get_payload_register
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.TFA.backup import gen_backup_codes
from src.lib.TFA.totp import GenTotpSecretReturnT, gen_totp_secret
from src.lib.algs.fernet import gen_fernet
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import pick
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.middleware.check_jwt import check_jwt_search_us_mdw
from src.models.token import TokenT
from src.models.user import User, UserDcT


async def get_msg_ctrl(req: Request) -> ResAPI:

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
    )


async def get_protected_data_ctrl(
    _: Request, us: UserDcT = Depends(check_jwt_search_us_mdw)
) -> ResAPI:
    return ResAPI.ok_200(msg="protected data 👻")


async def get_us_2FA_ctrl(req: Request) -> ResAPI:

    payload = get_payload_register()
    filtered = pick(payload, keys_off=["confirm_password"])

    q = req.state.parsed_q
    empty_codes = q.get("empty_codes")

    try:
        token_t = TokenT(q.get("cbc_hmac_t"))

    except Exception:
        raise ErrAPI(msg="invalid cbc_hmac_type", status=422)

    async with db_trx() as trx:

        us = User(**filtered, is_verified=True)
        await us.set_pwd(payload["password"])

        trx.add(us)
        await trx.flush([us])
        await trx.refresh(us)

        secret_result: GenTotpSecretReturnT = gen_totp_secret(
            user_email=us.email
        )
        us.totp_secret = gen_fernet(txt=secret_result["secret"])

        backup_codes: list[str] = []
        if not empty_codes:
            backup_codes = (await gen_backup_codes(trx, us_id=us.id))[
                "backup_codes_client"
            ]

        tokens_session = await gen_tokens_session(trx=trx, user_id=us.id)

        cbc_hmac_res = await gen_cbc_hmac(
            trx=trx, token_t=token_t, user_id=us.id
        )

        return ResAPI.ok_200(
            payload=payload,
            user=us,
            totp_secret=secret_result["secret"],
            backup_codes=backup_codes,
            access_token=tokens_session["access_token"],
            cbc_hmac_token=cbc_hmac_res["client_token"],
            cookies=[
                gen_refresh_cookie(
                    tokens_session["result_jwe"]["client_token"]
                )
            ],
        )
