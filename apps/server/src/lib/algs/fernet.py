from src.conf.env import get_env
from cryptography.fernet import Fernet

key_fernet: bytes = get_env().fernet_key.encode()


def enc_fernet(txt: bytes) -> bytes:
    encryptor = Fernet(key_fernet)
    return encryptor.encrypt(txt)


def dec_fernet(encrypted: bytes) -> bytes:
    decryptor = Fernet(key_fernet)
    return decryptor.decrypt(encrypted)
