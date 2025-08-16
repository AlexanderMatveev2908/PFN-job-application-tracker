from typing import Literal
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand


def derive_hkdf(
    *, master: bytes, info: bytes, salt: bytes
) -> dict[Literal["k_0", "k_1"], bytes]:
    h = hmac.HMAC(salt, hashes.SHA256())
    h.update(master)
    prk: bytes = h.finalize()

    okm: bytes = HKDFExpand(
        algorithm=hashes.SHA256(),
        length=64,
        info=info,
    ).derive(prk)

    return {"k_0": okm[:32], "k_1": okm[32:]}
