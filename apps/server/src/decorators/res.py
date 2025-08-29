from typing import Any, Literal, TypedDict, cast
from fastapi import Request
from fastapi.responses import JSONResponse

from src.lib.serialize_data import serialize


class CookieD(TypedDict, total=False):
    key: str
    value: str
    httponly: bool
    secure: bool
    samesite: Literal["lax", "strict", "none"]
    max_age: int
    path: str


CookieT = list[CookieD] | None
ClearCookieT = list[str | dict[str, CookieD]] | None


class ResAPI:
    def __init__(
        self,
        req: Request,
        cookies: CookieT = None,
        clear_cookies: ClearCookieT = None,
    ) -> None:
        self.req = req
        self.cookies = cookies or []
        self.clear_cookies = clear_cookies or []

    def _make(
        self,
        status: int,
        msg: str,
        data: dict[str, Any] | None = None,
    ) -> JSONResponse:
        payload = data or {}
        content = serialize(payload, max_depth=5)

        res = JSONResponse(
            status_code=status,
            content={
                **content,
                "msg": f"{'✅' if status in [200, 201, 204] else '💣'} {msg}",
            },
            headers=dict(getattr(self.req.state, "res_hdr", {})),
        )

        for c in self.cookies:
            res.set_cookie(**c)

        for cc in self.clear_cookies:
            res.delete_cookie(
                cast(str, cc if isinstance(cc, str) else cc["key"])
            )

        return res

    def ok_200(
        self,
        msg: str = "operation successful 📄",
        **kwargs: Any,
    ) -> JSONResponse:
        return self._make(
            200,
            msg,
            data=kwargs,
        )

    def ok_201(
        self,
        msg: str = "POST operation successful ✒️",
        **kwargs: Any,
    ) -> JSONResponse:
        return self._make(
            201,
            msg,
            data=kwargs,
        )

    def err_400(
        self, msg: str = "Bad request 😡", **kwargs: Any
    ) -> JSONResponse:
        return self._make(400, msg, data=kwargs)

    def err_401(
        self,
        msg: str = "Unauthorized 🔒",
        **kwargs: Any,
    ) -> JSONResponse:
        return self._make(
            401,
            msg,
            data=kwargs,
        )

    def err_403(
        self, msg: str = "Forbidden 🚫", **kwargs: Any
    ) -> JSONResponse:
        return self._make(403, msg, data=kwargs)

    def err_404(
        self, msg: str = "Not found 🥸", **kwargs: Any
    ) -> JSONResponse:
        return self._make(404, msg, data=kwargs)

    def err_409(self, msg: str = "Conflict 😵", **kwargs: Any) -> JSONResponse:
        return self._make(409, msg, data=kwargs)

    def err_422(
        self, msg: str = "Unprocessable entity 🧐", **kwargs: Any
    ) -> JSONResponse:
        return self._make(422, msg, data=kwargs)

    def err_429(
        self,
        msg: str = (
            "Our hamster-powered server took a break — try again later! 🐹"
        ),
        **kwargs: Any,
    ) -> JSONResponse:
        return self._make(
            429,
            msg,
            data=kwargs,
        )

    def err_500(
        self,
        msg: str = "A wild slime appeared — the server took 30% damage! ⚔️",
        **kwargs: Any,
    ) -> JSONResponse:
        return self._make(500, msg, data=kwargs)

    def err_ctm(
        self,
        status: int,
        msg: str,
        **kwargs: Any,
    ) -> JSONResponse:
        return self._make(
            status,
            msg,
            data=kwargs,
        )
