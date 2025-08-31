from importlib.resources import files
import re
import aiofiles
from src.decorators.err import ErrAPI


async def grab_html() -> str | None:
    p = str(files("src.lib.emails").joinpath("template.html"))

    txt = ""
    async with aiofiles.open(p, "r", encoding="utf-8") as f:
        txt = await f.read()

    parsed = re.search(
        r"<body[^>]*>(.*?)</body>", txt, re.DOTALL | re.IGNORECASE
    )

    return None if parsed is None else parsed.group(0)


async def gen_html_template(first_name: str, url: str) -> str:
    html = await grab_html()

    if not html:
        raise ErrAPI(msg="missing html email template", status=500)

    replacements = {
        "first_name": first_name,
        "url": url,
    }

    updated: str = html

    for k, v in replacements.items():
        updated = re.sub(rf"\${{{k}}}", v, updated)

    return updated
