import binascii
import json
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


def dec_aes_cbc(k: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
    dec = cipher.decryptor()
    padded = dec.update(ciphertext) + dec.finalize()

    unpadder = padding.PKCS7(BLOCK_BITS).unpadder()
    try:
        pt = unpadder.update(padded) + unpadder.finalize()
    except Exception:
        raise ErrAPI(msg="invalid ciphertext", status=401)
    return pt


def gen_sha256(
    mac_key: bytes, *, aad: bytes, iv: bytes, ciphertext: bytes
) -> bytes:
    h = chmac.HMAC(mac_key, hashes.SHA256())
    h.update(aad)
    h.update(iv)
    h.update(ciphertext)
    return h.finalize()


def constant_time_eq(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


CBC_K = "ad79b2e28912c7bf764c580ad44e0e315027f02738273f2379cc0b72739467c7"
SHA_K = "d231c215ed1350eb0f802cf2b30165af8334cf1b9c5ddc8ea50e6d0c33c39f6a"


payload = json.dumps({"id": 12345})


def handle_0() -> None:
    tup = gen_aes_cbc(binascii.unhexlify(CBC_K), payload.encode("utf-8"))

    for x in tup:
        print(x.hex())


RES_IV = "90d8d506b900ca7ed0d22514feb19b78"
RES_CT = "b0470d45951aa83b6e20e7e7766a966a"


def handle_1() -> None:
    pt = dec_aes_cbc(
        binascii.unhexlify(CBC_K),
        binascii.unhexlify(RES_IV),
        binascii.unhexlify(RES_CT),
    )

    print(pt.decode("utf-8"))


handle_1()
