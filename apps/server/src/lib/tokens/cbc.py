import os
from typing import Tuple
from src.decorators.err import ErrAPI
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


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
