from datetime import datetime, date
from enum import Enum
from typing import Any, Mapping, Optional, Sequence
import uuid
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import inspect


class ResAPI(JSONResponse):
    def __init__(
        self,
        status: int = 204,
        data: Optional[dict[str, Any]] = None,
    ) -> None:
        payload = data or {}
        max_depth: int = 10

        def _serialize(obj: Any, depth: int) -> Any:
            if depth > max_depth:
                return f"max_depth => {type(obj).__name__}"

            if obj is None or isinstance(obj, (bool, int, float, str)):
                return obj

            try:
                state = inspect(obj)
                if hasattr(state, "mapper"):
                    mapper = state.mapper
                    d: dict[str, Any] = {}

                    for col in mapper.columns:
                        v = getattr(obj, col.key)

                        if isinstance(v, uuid.UUID):
                            v = str(v)
                        elif isinstance(v, (datetime, date)):
                            v = v.isoformat()

                        d[col.key] = v
                    return _serialize(d, depth + 1)
            except Exception:
                pass

            if isinstance(obj, BaseModel):
                return _serialize(obj.model_dump(), depth + 1)

            if isinstance(obj, (bytes, bytearray)):
                try:
                    return obj.decode("utf-8")
                except Exception:
                    return list(obj)

            if isinstance(obj, (datetime, date)):
                return obj.isoformat()

            if isinstance(obj, Enum):
                return obj.value

            if isinstance(obj, (set)):
                return [_serialize(v, depth + 1) for v in obj]

            if isinstance(obj, Mapping):
                return {
                    str(k): _serialize(v, depth + 1) for k, v in obj.items()
                }

            if isinstance(obj, Sequence) and not isinstance(
                obj, (str, bytes, bytearray)
            ):
                return [_serialize(v, depth + 1) for v in obj]

            if hasattr(obj, "__dict__"):
                return _serialize(vars(obj), depth + 1)

            return obj

        content = _serialize(payload, depth=0)

        super().__init__(
            status_code=status,
            content=content,
        )

    @classmethod
    def ok_200(
        cls, msg: str = "GET operation successful ✅", **kwargs: Any
    ) -> "ResAPI":
        return cls(status=200, data={"msg": msg, **kwargs})

    @classmethod
    def ok_201(
        cls, msg: str = "POST operation successful ✅", **kwargs: Any
    ) -> "ResAPI":
        return cls(status=201, data={"msg": msg, **kwargs})

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
    ) -> "ResAPI":
        return cls(status=500, data={"msg": msg})

    @classmethod
    def err_ctm(cls, status: int, msg: str, *, data: dict = {}) -> "ResAPI":
        return cls(status, {"msg": msg, **data})
