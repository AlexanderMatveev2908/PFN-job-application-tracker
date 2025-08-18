from typing import Literal
from httpx import AsyncClient, Response

from src.lib.logger import clg


def parse_res(res: Response) -> dict:
    data = res.json()

    full = str(res.request.url)
    part = (
        full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203
    ).split("?", 1)[0]

    if res.status_code not in [200, 201]:
        clg(
            data,
            ttl=f"💾 {part} — 🚦 {res.status_code}",
        )

    return data


async def wrap_httpx(
    api: AsyncClient,
    *,
    url: str,
    method: Literal["POST", "GET"] = "POST",
    data: dict | None = None,
    expected_code: int = 200,
) -> tuple[dict, str]:

    if method == "POST":
        res = await api.post(url, json=data)
    elif method == "GET":
        res = await api.get(url)

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

    except Exception as err:
        clg(str(err), ttl="err assertion")
        raise err

    return (parsed, refresh)
