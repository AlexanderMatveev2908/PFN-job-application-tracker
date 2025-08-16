import json
import os
import hmac
from time import time
from typing import Any, Literal, cast
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_h, d_to_b, h_to_b
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import derive_hkdf_cbc_hmac
from src.lib.algs.hmac import gen_hmac


master_key = h_to_b(get_env().master_key)


def gen_cbc_sha(
    payload: dict[Literal["user_id"] | str, str], aad_d: dict
) -> str:

    shared_info = {
        **aad_d,
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

    tag: bytes = gen_hmac(
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

    comp_tag = gen_hmac(derived["k_1"], aad=aad, iv=iv, ciphertext=ct)

    if not constant_time_check(tag, comp_tag):
        raise ErrAPI(msg="invalid token", status=401)

    pt = dec_aes_cbc(derived["k_0"], iv=iv, ciphertext=ct)

    return json.loads(pt.decode("utf-8"))


print(
    gen_cbc_sha(
        {
            "user_id": "abcdef",
        },
        {"alg": "AES-CBC-HMAC-SHA256"},
    )
)
print(
    check_cbc_sha(
        "7b22616c67223a224145532d4342432d484d41432d534841323536222c22657870223a313735353333333535352c2273616c74223a2230396562386133323761663934656538353662343737376434313337313766633235626462383961326231643734633538363161306431336366626536616430222c22757365725f6964223a22616263646566227d.0f88922b9b0d31ff01946dfb8460397d.4f6af1d83260e611a1609376d5524660a62b74afdb4cf439121e5d769bf59f2b.631b70fdbe55ec24d5dd6d6d14e94b1141232254ce98b591cc540485191798e7"  # noqa: E501
    )
)
