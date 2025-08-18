from typing import Any
from httpx import AsyncClient, Response

from src.lib.logger import clg


def parse_res(res: Response) -> dict:
    data = res.json()

    full = str(res.request.url)
    part = full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203

    clg(
        data,
        ttl=f"💾 {part} — 🚦 {res.status_code}",
    )

    return data


async def wrap_httpx(
    api: AsyncClient, *, url: str, data: Any, expected_code: int = 200
) -> tuple[dict, str]:
    res = await api.post(url, json=data)

    assert res.status_code == expected_code

    parsed = parse_res(res)
    refresh = (
        res.cookies.get(
            "refresh_token",
        )
        or "N/A"
    )

    return (parsed, refresh)
