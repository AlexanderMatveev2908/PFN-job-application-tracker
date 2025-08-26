import io
import zipfile

import aiofiles

from src.lib.system import APP_DIR


async def TFA_zip_svc(
    totp_secret: str, backup_codes: list[str], binary_qr_code: bytes
) -> io.BytesIO:
    formatted: str = "\n".join(
        " ".join(backup_codes[i : i + 2])  # noqa: E203
        for i in range(0, len(backup_codes), 2)
    )

    buf = io.BytesIO()

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "backup_codes.txt",
            formatted,
        )
        zf.writestr("totp_secret.txt", totp_secret)
        zf.writestr(
            "qrcode.png",
            binary_qr_code,
        )

    assets_dir = APP_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    p = assets_dir / "test_2FA_data.zip"
    p.unlink(missing_ok=True)
    async with aiofiles.open(p, "wb") as f:
        buf.seek(0)
        await f.write(buf.read())

    return buf
