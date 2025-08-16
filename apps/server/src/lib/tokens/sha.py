from cryptography.hazmat.primitives import hashes, hmac


def gen_sha256(
    mac_key: bytes, *, aad: bytes, iv: bytes, ciphertext: bytes
) -> bytes:
    h = hmac.HMAC(mac_key, hashes.SHA256())
    h.update(aad)
    h.update(iv)
    h.update(ciphertext)
    return h.finalize()
