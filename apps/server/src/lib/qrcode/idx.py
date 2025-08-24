import base64
import io
from typing import TypedDict
import pyotp
import qrcode
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)


class GenQrcodeReturnT(TypedDict):
    base_64: str
    binary: bytes


def gen_qrcode(uri: str) -> GenQrcodeReturnT:

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=4,
    )

    qr.add_data(uri)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            front_color=(37, 99, 235),
            back_color=(255, 255, 255),
        ),
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    binary: bytes = buf.getvalue()

    # img_path = os.path.join("assets", f"{os.urandom(10).hex()}.png")
    # img.save(img_path, format="PNG")

    return {
        "base_64": base64.b64encode(binary).decode("utf-8"),
        "binary": binary,
    }
