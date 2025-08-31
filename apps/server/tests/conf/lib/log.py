from httpx import Response

from src.lib.logger import clg


def parse_res(res: Response, expected_code: int) -> dict:

    full = str(res.request.url)
    part = (
        full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203
    ).split("?", 1)[0]

    shorted: dict = {}

    data = {}

    if expected_code != 204:
        data = res.json()
        for k, v in data.items():
            shorted[k] = v[:100] if isinstance(v, str) else v

    if expected_code != res.status_code:
        clg(
            shorted,
            ttl=f"💾 {part} — 🚦 {res.status_code}",
        )

    return data
