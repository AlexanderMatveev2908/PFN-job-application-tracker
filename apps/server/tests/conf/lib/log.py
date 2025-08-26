from httpx import Response

from src.lib.logger import clg


def parse_res(res: Response) -> dict:
    data = res.json()

    full = str(res.request.url)
    part = (
        full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203
    ).split("?", 1)[0]

    shorted: dict = {}

    for k, v in data.items():
        shorted[k] = v[:100] if isinstance(v, str) else v

    clg(
        shorted,
        ttl=f"💾 {part} — 🚦 {res.status_code}",
    )

    return data
