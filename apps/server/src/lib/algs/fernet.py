from src.conf.env import get_env
from cryptography.fernet import Fernet

key_fernet: bytes = get_env().fernet_key.encode()


def gen_fernet(txt: str) -> bytes:
    encryptor = Fernet(key_fernet)
    return encryptor.encrypt(txt.encode())


def check_fernet(encrypted: bytes) -> bytes:
    decryptor = Fernet(key_fernet)
    return decryptor.decrypt(encrypted)
