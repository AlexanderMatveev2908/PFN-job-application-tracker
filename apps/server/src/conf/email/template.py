from pathlib import Path
import re
import aiofiles

from src.decorators.err import ErrAPI


async def grab_html() -> str | None:
    p = Path.cwd() / "src" / "conf" / "email" / "template.html"

    txt = ""
    async with aiofiles.open(p, "r", encoding="utf-8") as f:
        txt = await f.read()

    parsed = re.search(
        r"<body[^>]*>(.*?)</body>", txt, re.DOTALL | re.IGNORECASE
    )

    return None if parsed is None else parsed.group(0)


async def gen_html_template() -> str:
    html = await grab_html()

    if html is None:
        raise ErrAPI(msg="missing html email template", status=500)

    return re.sub(r"\$1", "John", html)
