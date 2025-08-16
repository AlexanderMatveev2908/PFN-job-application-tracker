import json
import os
import hmac
from time import time
from typing import Any, Literal, TypedDict, cast
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.algs.types import AlgT
from src.lib.data_structure import b_to_h, d_to_b, h_to_b
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import derive_hkdf_cbc_hmac
from src.lib.algs.hmac import hmac_from_cbc
from src.models.token import TokenT


master_key = h_to_b(get_env().master_key)


class InfoT(TypedDict):
    alg: AlgT
    token_t: TokenT


def gen_cbc_sha(
    payload: dict[Literal["user_id"] | str, str], aad_d: InfoT
) -> str:

    shared_info = {
        "alg": aad_d["alg"],
        "token_t": aad_d["token_t"].value,
        "user_id": payload["user_id"],
    }
    info: bytes = d_to_b(shared_info)

    salt: bytes = os.urandom(32)

    derived = derive_hkdf_cbc_hmac(master=master_key, info=info, salt=salt)

    aad: bytes = d_to_b(
        {
            **shared_info,
            "salt": b_to_h(salt),
            "exp": int(time()) + 15 * 60,
        }
    )

    iv, ct = gen_aes_cbc(derived["k_0"], d_to_b(cast(dict, payload)))

    tag: bytes = hmac_from_cbc(
        derived["k_1"],
        aad=aad,
        iv=iv,
        ciphertext=ct,
    )

    return f"{b_to_h(aad)}.{b_to_h(iv)}.{b_to_h(ct)}.{b_to_h(tag)}"


def constant_time_check(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


def check_cbc_sha(token: str) -> dict[str, Any]:

    try:
        aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")
    except Exception:
        raise ErrAPI(msg="invalid token format", status=401)

    aad_d: dict = json.loads(h_to_b(aad_hex).decode("utf-8"))

    if int(aad_d["exp"]) <= int(time()):
        raise ErrAPI(msg="expired token", status=401)

    info_b: bytes = d_to_b(
        {
            "alg": aad_d["alg"],
            "token_t": aad_d["token_t"],
            "user_id": aad_d["user_id"],
        }
    )

    derived = derive_hkdf_cbc_hmac(
        master=master_key,
        info=info_b,
        salt=h_to_b(aad_d["salt"]),
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


print(
    gen_cbc_sha(
        {
            "user_id": "abcdef",
        },
        {"alg": "AES-CBC-HMAC-SHA256", "token_t": TokenT.CHANGE_EMAIL},
    )
)
print(
    check_cbc_sha(
        "7b22616c67223a224145532d4342432d484d41432d534841323536222c22657870223a313735353333353832302c2273616c74223a2261656533653464343465633665633961383132623164613334356433643430633266653766386364643834656232306337653463363234633163336561333162222c22746f6b656e5f74223a224348414e47455f454d41494c222c22757365725f6964223a22616263646566227d.6ece8c49dfcf3e3e3700a7335fa6c1a5.2d96bde0d388ea12b4e224dc0cf8a3ce8c8d1a352de0cdc1f0aff2d4f8bfb667.06101946572e582777a5d8e60f86d46a22a609488fe5429a840430aeb7228a5a"  # noqa: E501
    )
)
