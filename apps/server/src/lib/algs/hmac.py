from cryptography.hazmat.primitives import hashes, hmac as chmac
import hmac
from src.conf.env import get_env
from src.lib.data_structure import h_to_b


def gen_hmac(mac_key: bytes, pt: bytes) -> bytes:
    h = chmac.HMAC(mac_key, hashes.SHA256())
    h.update(pt)
    return h.finalize()


def hash_db_hmac(tok: bytes) -> bytes:
    pepper = h_to_b(get_env().pepper_hmac_key)

    return gen_hmac(mac_key=pepper, pt=tok)


def check_hmac(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)
