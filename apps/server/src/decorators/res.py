from typing import Any, Literal, TypedDict, cast
from fastapi import Request, Response
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

    def _apply_cookies(self, res: Response) -> None:
        for c in self.cookies:
            res.set_cookie(**c)
        for cc in self.clear_cookies:
            res.delete_cookie(
                cast(str, cc if isinstance(cc, str) else cc["key"])
            )

    def _make(
        self,
        status: int,
        msg: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        payload = data or {}
        content = serialize(payload, max_depth=5)

        if msg:
            content["msg"] = f"{'✅' if status in [200, 201] else '💣'} {msg}"

        base_hdr = dict(getattr(self.req.state, "res_hdr", {}))

        if status == 204:
            res = Response(status_code=204, headers=base_hdr)
        else:
            res = JSONResponse(
                status_code=status,
                content=content,
                headers=base_hdr,
            )

        self._apply_cookies(res)

        return res

    def ok_200(
        self,
        msg: str = "operation successful 📄",
        **kwargs: Any,
    ) -> Response:
        return self._make(
            200,
            msg,
            data=kwargs,
        )

    def ok_201(
        self,
        msg: str = "POST operation successful ✒️",
        **kwargs: Any,
    ) -> Response:
        return self._make(
            201,
            msg,
            data=kwargs,
        )

    def ok_204(self) -> Response:
        return self._make(
            204,
        )

    def err_400(self, msg: str = "Bad request 😡", **kwargs: Any) -> Response:
        return self._make(400, msg, data=kwargs)

    def err_401(
        self,
        msg: str = "Unauthorized 🔒",
        **kwargs: Any,
    ) -> Response:
        return self._make(
            401,
            msg,
            data=kwargs,
        )

    def err_403(self, msg: str = "Forbidden 🚫", **kwargs: Any) -> Response:
        return self._make(403, msg, data=kwargs)

    def err_404(self, msg: str = "Not found 🥸", **kwargs: Any) -> Response:
        return self._make(404, msg, data=kwargs)

    def err_409(self, msg: str = "Conflict 😵", **kwargs: Any) -> Response:
        return self._make(409, msg, data=kwargs)

    def err_422(
        self, msg: str = "Unprocessable entity 🧐", **kwargs: Any
    ) -> Response:
        return self._make(422, msg, data=kwargs)

    def err_429(
        self,
        msg: str = (
            "Our hamster-powered server took a break — try again later! 🐹"
        ),
        **kwargs: Any,
    ) -> Response:
        return self._make(
            429,
            msg,
            data=kwargs,
        )

    def err_500(
        self,
        msg: str = "A wild slime appeared — the server took 30% damage! ⚔️",
        **kwargs: Any,
    ) -> Response:
        return self._make(500, msg, data=kwargs)

    def err_ctm(
        self,
        status: int,
        msg: str,
        **kwargs: Any,
    ) -> Response:
        return self._make(
            status,
            msg,
            data=kwargs,
        )
