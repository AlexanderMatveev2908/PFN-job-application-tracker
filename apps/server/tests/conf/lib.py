from httpx import Response

from src.lib.logger import clg


def parse_res(res: Response) -> dict:
    data = res.json()

    full = str(res.request.url)
    part = full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203

    clg(
        data,
        res.cookies.get("refresh_token", "N/A refresh_token"),
        ttl=f"💾 {part} — 🚦 {res.status_code}",
    )

    return data
