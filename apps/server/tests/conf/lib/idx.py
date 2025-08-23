from typing import Any, Literal, TypedDict

from httpx import AsyncClient

from tests.conf.lib.log import parse_res


class WrapReturnT(TypedDict):
    data: dict[Literal["msg"] | str, Any]
    refresh_token: str


async def wrap_httpx(
    api: AsyncClient,
    *,
    url: str,
    method: Literal["POST", "GET"] = "POST",
    data: Any | None = None,
    access_token: str = "",
    expected_code: int = 200,
) -> WrapReturnT:

    methods = {
        "GET": api.get,
        "POST": api.post,
        "PUT": api.put,
        "DELETE": api.delete,
    }

    res = await methods[method](
        url,
        json=data if method in {"POST", "PUT"} else None,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    parsed = parse_res(res)
    refresh = (
        res.cookies.get(
            "refresh_token",
        )
        or "N/A"
    )

    try:
        assert (
            res.status_code == expected_code
        ), f"❌ got {res.status_code} • expected {expected_code}"

    except Exception:
        raise

    return {
        "data": parsed,
        "refresh_token": refresh,
    }
