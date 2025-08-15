import traceback
from typing import Any, Literal, Mapping, Optional, TypedDict, cast
from fastapi.responses import JSONResponse
from src.lib.data_structure import serialize
from src.lib.logger import clg


class CookieD(TypedDict, total=False):
    key: str
    value: str
    httponly: bool
    secure: bool
    samesite: Literal["lax", "strict", "none"]
    max_age: int
    path: str


CookieT = Optional[list[CookieD]]
ClearCookieT = Optional[list[str | dict[str, Any]]]


class ResAPI(JSONResponse):
    def __init__(
        self,
        status: int = 204,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        cookies: CookieT = None,
        clear_cookies: ClearCookieT = None,
    ) -> None:
        payload = data or {}

        content = serialize(payload, depth=0, max_depth=5)

        super().__init__(
            status_code=status,
            content={
                **content,
            },
            # content={
            #     **content,
            #     **{k: v for k, v in (headers or {}).items()},
            # },
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
        msg: str = "GET operation successful ✅",
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
        msg: str = "POST operation successful ✅",
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
    def err_401(cls, msg: str = "Unauthorized 🔒", **kwargs: Any) -> "ResAPI":
        return cls(status=401, data={"msg": msg, **kwargs})

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
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(status=429, data={"msg": msg, **kwargs})

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
        **kwargs: Any,
    ) -> "ResAPI":
        return cls(status=status, data={"msg": msg, **kwargs}, headers=headers)

    @staticmethod
    def _log(err: Exception) -> None:
        frames = traceback.extract_tb(err.__traceback__)
        src_frames = []

        for f in frames:
            if "src/" in f.filename:
                src_frames.append(
                    f"📂 {f.filename} => 🔢 {f.lineno}"
                    f" | 🆎 {f.name} | ☢️ {f.line}"
                )

        clg(
            *src_frames,
            "\t",
            ttl=f"💣 {type(err).__name__}",
        )
