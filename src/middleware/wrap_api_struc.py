from typing import Awaitable, Callable

from fastapi import HTTPException, Request

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.logger import log


def wrap_api(cb_ctrl: Callable[[Request], Awaitable]) -> Callable:

    async def wrap(req: Request) -> "ResAPI" | Callable:
        try:
            return await cb_ctrl(req)
        except Exception as err:
            log(err, ttl="err wrap api")

            opt = None

            if isinstance(err, HTTPException):
                status = err.status_code
                msg = err.detail
            elif isinstance(err, ErrAPI):
                status = err.status
                msg = err.msg
                opt = getattr(err, "opt", None)
            else:
                status = 500
                msg = str(err)

            return ResAPI.err_ctm(status=status, msg=msg, opt=opt)

    return wrap
