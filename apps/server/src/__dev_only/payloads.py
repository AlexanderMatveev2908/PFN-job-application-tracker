from typing import TypedDict

from faker import Faker
from src.lib.pwd_gen import gen_pwd

faker = Faker()


class RegisterPayloadT(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    terms: bool


def get_payload_register() -> RegisterPayloadT:
    pwd = gen_pwd(enc="utf-8", n=5)
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": pwd,
        "confirm_password": pwd,
        "terms": True,
    }
