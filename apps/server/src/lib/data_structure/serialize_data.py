from collections.abc import Mapping, Sequence, Iterable
from typing import Any, Optional, cast
from datetime import date, datetime
from enum import Enum
import uuid
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm.state import InstanceState
from sqlalchemy.orm import Mapper

from src.lib.logger import clg  # noqa: F401


def serialize(
    obj: Any,
    *,
    max_depth: int = 0,
    join: bool = False,
    exclude_keys: Optional[Iterable[str]] = None,
) -> Any:
    return _ser(
        obj,
        depth=0,
        max_depth=max_depth,
        join=join,
        exclude=set(exclude_keys or []),
        seen=set(),
    )


def serialize_tricky(v: Any) -> Any:
    if isinstance(v, uuid.UUID):
        return str(v)
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, Enum):
        return v.value
    if isinstance(v, (bytes, bytearray)):
        try:
            return v.hex()
        except Exception:
            return "👻"
    return v


def _ser(
    obj: Any,
    *,
    depth: int,
    max_depth: int,
    join: bool,
    exclude: set[str],
    seen: set[int],
) -> Any:
    if depth > max_depth:
        return f"reached_max_depth => {type(obj).__name__}"

    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    obj_id = id(obj)
    if obj_id in seen:
        return f"circular_ref => {type(obj).__name__}"

    track = isinstance(obj, (Mapping, Sequence)) or hasattr(obj, "__dict__")
    if track:
        seen.add(obj_id)

    try:
        state = inspect(obj)

        if hasattr(state, "mapper"):
            istate = cast(InstanceState[Any], state)
            mapper: Mapper[Any] = istate.mapper
            sd = istate.dict

            out: dict[str, Any] = {}

            for col in mapper.columns:
                k = col.key
                if k in exclude or k not in sd:
                    continue
                out[k] = serialize_tricky(sd[k])

            if join and depth < max_depth:
                for rel in mapper.relationships:
                    k = rel.key
                    if k in exclude or k not in sd:
                        continue
                    v = sd[k]
                    if v is None:
                        out[k] = None
                    elif rel.uselist:
                        out[k] = [
                            _ser(
                                item,
                                depth=depth + 1,
                                max_depth=max_depth,
                                join=join,
                                exclude=exclude,
                                seen=seen,
                            )
                            for item in v
                        ]
                    else:
                        out[k] = _ser(
                            v,
                            depth=depth + 1,
                            max_depth=max_depth,
                            join=join,
                            exclude=exclude,
                            seen=seen,
                        )
            return out
    except Exception:
        # clg(err, ttl="err serialize data")
        pass

    if isinstance(obj, BaseModel):
        return _ser(
            obj.model_dump(),
            depth=depth + 1,
            max_depth=max_depth,
            join=join,
            exclude=exclude,
            seen=seen,
        )

    nv = serialize_tricky(obj)
    if nv is not obj:
        return nv

    if isinstance(obj, Mapping):
        return {
            str(k): _ser(
                v,
                depth=depth + 1,
                max_depth=max_depth,
                join=join,
                exclude=exclude,
                seen=seen,
            )
            for k, v in obj.items()
            if str(k) not in exclude
        }

    if isinstance(obj, Sequence) and not isinstance(
        obj, (str, bytes, bytearray)
    ):
        return [
            _ser(
                v,
                depth=depth + 1,
                max_depth=max_depth,
                join=join,
                exclude=exclude,
                seen=seen,
            )
            for v in obj
        ]

    if hasattr(obj, "__dict__"):
        return _ser(
            vars(obj),
            depth=depth + 1,
            max_depth=max_depth,
            join=join,
            exclude=exclude,
            seen=seen,
        )

    return obj
