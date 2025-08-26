import os
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
    first_name = faker.first_name()
    return {
        "first_name": first_name,
        "last_name": faker.last_name(),
        "email": f"{first_name}-{os.urandom(10).hex()}&@gmail.com",
        "password": pwd,
        "confirm_password": pwd,
        "terms": True,
    }
