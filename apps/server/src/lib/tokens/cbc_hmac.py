import json
import os
import hmac
from time import time
from typing import Any, Literal, TypedDict, cast
import uuid
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_h, d_to_b, h_to_b
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import DerivedKeysCbcHmacT, derive_hkdf_cbc_hmac
from src.lib.algs.hmac import hmac_from_cbc
from src.models.token import AlgT, TokenT


master_key = h_to_b(get_env().master_key)


class HdrT(TypedDict):
    alg: AlgT
    token_t: TokenT


class CbcHmacResT(TypedDict):
    client_token: str
    token_id: uuid.UUID


async def gen_cbc_hmac(
    payload: dict[Literal["user_id"] | str, str], hdr: HdrT
) -> CbcHmacResT:

    info_d: dict = {
        "alg": hdr["alg"].value,
        "token_t": hdr["token_t"].value,
        "user_id": payload["user_id"],
    }

    info: bytes = d_to_b(info_d)
    salt: bytes = os.urandom(32)

    derived: DerivedKeysCbcHmacT = derive_hkdf_cbc_hmac(
        master=master_key, info=info, salt=salt
    )
    token_id: uuid.UUID = uuid.uuid4()

    aad: bytes = d_to_b(
        {
            **info_d,
            "token_id": str(token_id),
            "salt": b_to_h(salt),
        }
    )

    iv, ct = gen_aes_cbc(derived["k_0"], d_to_b(cast(dict, payload)))

    tag: bytes = hmac_from_cbc(
        derived["k_1"],
        aad=aad,
        iv=iv,
        ciphertext=ct,
    )

    return {
        "client_token": f"{b_to_h(aad)}.{b_to_h(iv)}.{b_to_h(ct)}.{b_to_h(tag)}",  # noqa: E501
        "token_id": token_id,
    }


def constant_time_check(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


def check_cbc_hmac(token: str) -> dict[str, Any]:

    try:
        aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")
    except Exception:
        raise ErrAPI(msg="invalid token format", status=401)

    hdr: dict = json.loads(h_to_b(aad_hex).decode("utf-8"))

    if int(hdr["exp"]) <= int(time()):
        raise ErrAPI(msg="expired token", status=401)

    info_b: bytes = d_to_b(
        {
            "alg": hdr["alg"],
            "token_t": hdr["token_t"],
            "user_id": hdr["user_id"],
        }
    )

    derived = derive_hkdf_cbc_hmac(
        master=master_key,
        info=info_b,
        salt=h_to_b(hdr["salt"]),
    )

    aad: bytes = h_to_b(aad_hex)
    iv: bytes = h_to_b(iv_hex)
    ct: bytes = h_to_b(ct_hex)
    tag: bytes = h_to_b(tag_hex)

    comp_tag = hmac_from_cbc(derived["k_1"], aad=aad, iv=iv, ciphertext=ct)

    if not constant_time_check(tag, comp_tag):
        raise ErrAPI(msg="invalid token", status=401)

    pt = dec_aes_cbc(derived["k_0"], iv=iv, ciphertext=ct)

    return json.loads(pt.decode("utf-8"))
