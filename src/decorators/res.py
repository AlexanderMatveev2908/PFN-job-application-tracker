from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse


class AppRes(JSONResponse):
    def __init__(
        self,
        status: int = 204,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        data = data or {}
        super().__init__(status_code=status, content=data)

    @classmethod
    def ok_200(
        cls, msg: str = "GET operation successful ✅", **kwargs
    ) -> "AppRes":
        return cls(status=200, data={"msg": msg, **kwargs})

    @classmethod
    def ok_201(
        cls, msg: str = "POST operation successful ✅", **kwargs
    ) -> "AppRes":
        return cls(status=201, data={"msg": msg, **kwargs})

    @classmethod
    def err_400(cls, msg: str = "Bad request 😡") -> "AppRes":
        return cls(status=400, data={"msg": msg})

    @classmethod
    def err_401(cls, msg: str = "Unauthorized 🔒") -> "AppRes":
        return cls(status=401, data={"msg": msg})

    @classmethod
    def err_403(cls, msg: str = "Forbidden 🚫") -> "AppRes":
        return cls(status=403, data={"msg": msg})

    @classmethod
    def err_404(cls, msg: str = "Not found 🥸") -> "AppRes":
        return cls(status=404, data={"msg": msg})

    @classmethod
    def err_409(cls, msg: str = "Conflict 😵") -> "AppRes":
        return cls(status=409, data={"msg": msg})

    @classmethod
    def err_422(cls, msg: str = "Unprocessable entity 🧐") -> "AppRes":
        return cls(status=422, data={"msg": msg})

    @classmethod
    def err_429(
        cls,
        msg: str = "Our hamster-powered server took a break"
        " — try again later! 🐹",
    ) -> "AppRes":
        return cls(status=429, data={"msg": msg})

    @classmethod
    def err_500(
        cls,
        msg: str = "A wild slime appeared" " — the server took 30% damage! ⚔️",
    ) -> "AppRes":
        return cls(status=500, data={"msg": msg})
