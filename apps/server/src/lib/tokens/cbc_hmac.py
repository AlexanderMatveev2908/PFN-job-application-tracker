from __future__ import annotations

import os
import hmac
from typing import Tuple

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac as chmac, padding

from src.decorators.err import ErrAPI

BLOCK_BITS = 128


def gen_aes_cbc(k: bytes, plain_txt: bytes) -> Tuple[bytes, bytes]:
    if len(k) not in (16, 24, 32):
        raise ErrAPI(msg="k not in range 16 • 24 • 32", status=500)

    iv = os.urandom(16)
    padder = padding.PKCS7(BLOCK_BITS).padder()
    padded = padder.update(plain_txt) + padder.finalize()

    cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
    enc = cipher.encryptor()
    ct = enc.update(padded) + enc.finalize()
    return iv, ct


def aes_cbc_decrypt(k: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
    dec = cipher.decryptor()
    padded = dec.update(ciphertext) + dec.finalize()

    unpadder = padding.PKCS7(BLOCK_BITS).unpadder()
    try:
        pt = unpadder.update(padded) + unpadder.finalize()
    except Exception:
        raise ErrAPI(msg="invalid ciphertext", status=401)
    return pt


def hmac_sha256(
    mac_key: bytes, *, aad: bytes, iv: bytes, ciphertext: bytes
) -> bytes:
    h = chmac.HMAC(mac_key, hashes.SHA256())
    h.update(aad)
    h.update(iv)
    h.update(ciphertext)
    return h.finalize()


def constant_time_eq(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)
