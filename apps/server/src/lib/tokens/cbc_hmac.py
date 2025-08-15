import json
import os
import hmac
from typing import Tuple

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac as chmac, padding

from src.decorators.err import ErrAPI

BLOCK_BITS = 128
ALG = "AES-CBC-HMAC-SHA256"


def to_b(txt_hex: str) -> bytes:
    return bytes.fromhex(txt_hex)


def to_h(b: bytes) -> str:
    return b.hex()


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


def gen_sha256(
    mac_key: bytes, *, aad: bytes, iv: bytes, ciphertext: bytes
) -> bytes:
    h = chmac.HMAC(mac_key, hashes.SHA256())
    h.update(aad)
    h.update(iv)
    h.update(ciphertext)
    return h.finalize()


CBC_K = "ad79b2e28912c7bf764c580ad44e0e315027f02738273f2379cc0b72739467c7"
SHA_K = "d231c215ed1350eb0f802cf2b30165af8334cf1b9c5ddc8ea50e6d0c33c39f6a"

payload: bytes = json.dumps({"id": 12345}).encode("utf-8")


def gen_cbc_sha() -> str:
    iv, ct = gen_aes_cbc(to_b(CBC_K), payload)

    aad = json.dumps({"alg": ALG, "id": "abc"}).encode("utf-8")

    hdr = gen_sha256(
        to_b(SHA_K),
        aad=aad,
        iv=iv,
        ciphertext=ct,
    )

    return f"{to_h(aad)}.{to_h(iv)}.{to_h(ct)}.{to_h(hdr)}"


def constant_time_check(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


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


def check_cbc_sha(token: str) -> str:
    aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")

    aad = to_b(aad_hex)
    iv = to_b(iv_hex)
    ct = to_b(ct_hex)
    tag = to_b(tag_hex)

    comp_tag = gen_sha256(to_b(SHA_K), aad=aad, iv=iv, ciphertext=ct)

    if not constant_time_check(tag, comp_tag):
        raise ErrAPI(msg="invalid token", status=401)

    pt = dec_aes_cbc(to_b(CBC_K), iv=iv, ciphertext=ct)

    return json.loads(pt.decode("utf-8"))


print(gen_cbc_sha())
print(
    check_cbc_sha(
        "7b22616c67223a20224145532d4342432d484d41432d534841323536222c20226964223a2022616263227d.a3225deb9905a7ac43976292075ed696.19ae388e00f5b1afb5b0471d4eefceb4.3477599d83340d6f17008ea49ca3311d9a9c436ef5aff12f7e97dedb2ddcad16"
    )
)
