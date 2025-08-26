from typing import Literal, cast

from src.__dev_only.payloads import RegisterPayloadT
from src.lib.data_structure import b_to_d, h_to_b
from src.lib.tokens.cbc_hmac import AadT
from src.models.token import TokenT


def extract_login_payload(
    payload_register: RegisterPayloadT,
) -> dict[Literal["email", "password"], str]:
    return {
        "email": payload_register["email"],
        "password": payload_register["password"],
    }


def get_aad_cbc_hmac(token: str, token_t: TokenT) -> AadT:
    parsed: dict = b_to_d(h_to_b(token.split(".")[0]))

    assert TokenT(parsed["token_t"]) == token_t

    return cast(AadT, parsed)
