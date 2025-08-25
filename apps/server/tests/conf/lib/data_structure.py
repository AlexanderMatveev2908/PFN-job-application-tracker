from typing import Literal

from src.__dev_only.payloads import RegisterPayloadT


def extract_login_payload(
    payload_register: RegisterPayloadT,
) -> dict[Literal["email", "password"], str]:
    return {
        "email": payload_register["email"],
        "password": payload_register["password"],
    }
