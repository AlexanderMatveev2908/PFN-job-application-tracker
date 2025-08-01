from typing import Any, Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ResAPI(JSONResponse):
    def __init__(
        self,
        status: int = 204,
        data: Optional[dict[str, Any]] = None,
    ) -> None:
        data = data or {}

        for k, v in data.items():
            if isinstance(v, BaseModel):
                data[k] = v.model_dump()

        super().__init__(status_code=status, content=data)

    @classmethod
    def ok_200(
        cls, msg: str = "GET operation successful ✅", **kwargs
    ) -> "ResAPI":
        return cls(status=200, data={"msg": msg, **kwargs})

    @classmethod
    def ok_201(
        cls, msg: str = "POST operation successful ✅", **kwargs
    ) -> "ResAPI":
        return cls(status=201, data={"msg": msg, **kwargs})

    @classmethod
    def err_400(cls, msg: str = "Bad request 😡") -> "ResAPI":
        return cls(status=400, data={"msg": msg})

    @classmethod
    def err_401(cls, msg: str = "Unauthorized 🔒") -> "ResAPI":
        return cls(status=401, data={"msg": msg})

    @classmethod
    def err_403(cls, msg: str = "Forbidden 🚫") -> "ResAPI":
        return cls(status=403, data={"msg": msg})

    @classmethod
    def err_404(cls, msg: str = "Not found 🥸") -> "ResAPI":
        return cls(status=404, data={"msg": msg})

    @classmethod
    def err_409(cls, msg: str = "Conflict 😵") -> "ResAPI":
        return cls(status=409, data={"msg": msg})

    @classmethod
    def err_422(
        cls, msg: str = "Unprocessable entity 🧐", **kwargs
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
    ) -> "ResAPI":
        return cls(status=429, data={"msg": msg})

    @classmethod
    def err_500(
        cls,
        msg: str = "A wild slime appeared" " — the server took 30% damage! ⚔️",
    ) -> "ResAPI":
        return cls(status=500, data={"msg": msg})

    @classmethod
    def err_ctm(
        cls, status: int, msg: str, *, data: dict | None = None
    ) -> "ResAPI":
        return cls(status, {"msg": msg, **(data or {})})
