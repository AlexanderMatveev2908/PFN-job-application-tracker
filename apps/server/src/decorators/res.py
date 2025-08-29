from typing import Any, Literal, Mapping, Optional, TypedDict, cast
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


class ResAPIProt:
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


class ResAPI(JSONResponse):
    def __init__(
        self,
        status: int,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        cookies: CookieT = None,
        clear_cookies: ClearCookieT = None,
    ) -> None:
        payload = data or {}

        content = serialize(payload, max_depth=5)

        super().__init__(
            status_code=status,
            content={
                **content,
                "msg": f"{'✅' if status in [200, 201, 204] else '💣'} {content['msg']}",  # noqa: E501
            },
            headers=headers,
        )

        if cookies:
            for c in cookies:
                self.set_cookie(**c)

        if clear_cookies:
            for cc in clear_cookies:
                if isinstance(cc, str):
                    self.delete_cookie(cast(str, cc))
                else:
                    self.delete_cookie(cast(dict, cc)["key"])

    @classmethod
    def ok_200(
        cls,
        msg: str = "operation successful 📄",
        cookies: CookieT = None,
        clear_cookies: ClearCookieT = None,
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(
            status=200,
            cookies=cookies,
            clear_cookies=clear_cookies,
            data={"msg": msg, **kwargs},
        )

    @classmethod
    def ok_201(
        cls,
        msg: str = "POST operation successful ✒️",
        cookies: CookieT = None,
        clear_cookies: ClearCookieT = None,
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(
            status=201,
            cookies=cookies,
            clear_cookies=clear_cookies,
            data={"msg": msg, **kwargs},
        )

    @classmethod
    def err_400(cls, msg: str = "Bad request 😡", **kwargs: Any) -> "ResAPI":
        return cls(status=400, data={"msg": msg, **kwargs})

    @classmethod
    def err_401(
        cls,
        msg: str = "Unauthorized 🔒",
        clear_cookies: ClearCookieT = None,
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(
            status=401,
            clear_cookies=clear_cookies,
            data={"msg": msg, **kwargs},
        )

    @classmethod
    def err_403(cls, msg: str = "Forbidden 🚫", **kwargs: Any) -> "ResAPI":
        return cls(status=403, data={"msg": msg, **kwargs})

    @classmethod
    def err_404(cls, msg: str = "Not found 🥸", **kwargs: Any) -> "ResAPI":
        return cls(status=404, data={"msg": msg, **kwargs})

    @classmethod
    def err_409(cls, msg: str = "Conflict 😵", **kwargs: Any) -> "ResAPI":
        return cls(status=409, data={"msg": msg, **kwargs})

    @classmethod
    def err_422(
        cls, msg: str = "Unprocessable entity 🧐", **kwargs: Any
    ) -> "ResAPI":
        return cls(
            status=422,
            data={"msg": msg, **kwargs},
        )

    @classmethod
    def err_429(
        cls,
        msg: str = "Our hamster-powered server took a break"
        " — try again later! 🐹",
        clear_cookies: ClearCookieT = None,
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(
            status=429,
            clear_cookies=clear_cookies,
            data={"msg": msg, **kwargs},
        )

    @classmethod
    def err_500(
        cls,
        msg: str = "A wild slime appeared" " — the server took 30% damage! ⚔️",
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(status=500, data={"msg": msg, **kwargs})

    @classmethod
    def err_ctm(
        cls,
        status: int,
        msg: str,
        headers: Optional[Mapping[str, str]] = None,
        cookies: CookieT = None,
        clear_cookies: ClearCookieT = None,
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(
            status=status,
            cookies=cookies,
            clear_cookies=clear_cookies,
            headers=headers,
            data={"msg": msg, **kwargs},
        )
