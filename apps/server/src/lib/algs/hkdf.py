from typing import Literal
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand

from src.lib.data_structure import h_to_b


MASTERS: dict[int, bytes] = {
    0: h_to_b(
        "bdbbc28606c8c51f58a3bf38ae2d94042a07f3651fb585691440895595b42d8e0edc4dbbf73f4ccb89e76acb92a9c50d59742524c0eec7026cfb096cdb257d6a"  # noqa: E501
    )
}


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
