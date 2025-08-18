import os
from typing import TypedDict


class RegisterPayloadT(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    terms: bool


def get_payload_register() -> RegisterPayloadT:
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"{os.urandom(16).hex()}@gmail.com",
        "password": "qcxd-0KK64BVu5Z84DY5@czE6{!^zI_a2e9^{P(#",
        "confirm_password": "qcxd-0KK64BVu5Z84DY5@czE6{!^zI_a2e9^{P(#",
        "terms": True,
    }
