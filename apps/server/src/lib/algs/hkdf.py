from typing import Literal
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand


def extract_prk(master: bytes, salt: bytes) -> bytes:
    h = hmac.HMAC(salt, hashes.SHA256())
    h.update(master)
    prk: bytes = h.finalize()

    return prk


def expand_okm(prk: bytes, length: int, info: bytes) -> bytes:

    okm: bytes = HKDFExpand(
        algorithm=hashes.SHA256(),
        length=length,
        info=info,
    ).derive(prk)

    return okm


def derive_hkdf_cbc_hmac(
    *, master: bytes, info: bytes, salt: bytes
) -> dict[Literal["k_0", "k_1"], bytes]:
    prk = extract_prk(master, salt)

    okm = expand_okm(prk, length=64, info=info)

    return {"k_0": okm[:32], "k_1": okm[32:]}


def derive_hmac(master: bytes, salt: bytes, info: bytes) -> bytes:
    prk = extract_prk(master, salt)

    okm = expand_okm(prk, length=32, info=info)

    return okm
