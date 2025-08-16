from cryptography.hazmat.primitives import hashes, hmac


def hmac_from_cbc(
    mac_key: bytes, *, aad: bytes, iv: bytes, ciphertext: bytes
) -> bytes:
    h = hmac.HMAC(mac_key, hashes.SHA256())
    h.update(aad)
    h.update(iv)
    h.update(ciphertext)
    return h.finalize()


def gen_hmac(mac_key: bytes, pt: bytes) -> bytes:
    h = hmac.HMAC(mac_key, hashes.SHA256())

    h.update(pt)
    return h.finalize()
