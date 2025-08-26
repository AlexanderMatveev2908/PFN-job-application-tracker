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
    method: Literal["POST", "GET", "PUT", "PATCH", "DELETE"] = "POST",
    data: Any | None = None,
    access_token: str = "",
    expected_code: int = 200,
) -> WrapReturnT:

    h = {"authorization": f"Bearer {access_token}"}

    fn = getattr(api, method.lower())
    kwargs = {
        "url": url,
        "headers": h,
    }
    if method in ["POST", "PUT", "PATCH"]:
        kwargs["json"] = data
    res = await fn(**kwargs)

    parsed = parse_res(res, expected_code=expected_code)
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
