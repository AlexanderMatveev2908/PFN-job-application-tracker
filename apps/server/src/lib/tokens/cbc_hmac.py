import json
import os
import hmac
from time import time
from typing import Any
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_d, b_to_h, d_to_b, h_to_b
from src.lib.tokens.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.tokens.hkdf import MASTERS, derive_hkdf
from src.lib.tokens.sha import gen_sha256


ALG = "AES-CBC-HMAC-SHA256"


def gen_cbc_sha() -> str:

    payload: bytes = d_to_b({"id": "12345"})
    payload_utf_8 = b_to_d(payload)
    v = "0"
    shared_info = {
        "alg": ALG,
        "v": v,
        "user_id": payload_utf_8["id"],
    }
    info = d_to_b(shared_info)

    salt = os.urandom(32)

    derived = derive_hkdf(master=MASTERS[0], info=info, salt=salt)

    aad = d_to_b(
        {
            **shared_info,
            "salt": b_to_h(salt),
            "exp": int(time()) + 15 * 60,
        }
    )

    iv, ct = gen_aes_cbc(derived["k_0"], payload)

    tag = gen_sha256(
        derived["k_1"],
        aad=aad,
        iv=iv,
        ciphertext=ct,
    )

    return f"{b_to_h(aad)}.{b_to_h(iv)}.{b_to_h(ct)}.{b_to_h(tag)}"


def constant_time_check(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


def check_cbc_sha(token: str) -> dict[str, Any]:

    aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")

    aad_d: dict = json.loads(h_to_b(aad_hex).decode("utf-8"))

    if int(aad_d["exp"]) < int(time()):
        raise ErrAPI(msg="expired token", status=401)

    info_b: bytes = d_to_b(
        {
            "alg": aad_d["alg"],
            "v": aad_d["v"],
            "user_id": aad_d["user_id"],
        }
    )

    derived = derive_hkdf(
        master=MASTERS[0],
        info=info_b,
        salt=h_to_b(aad_d["salt"]),
    )

    aad: bytes = h_to_b(aad_hex)
    iv: bytes = h_to_b(iv_hex)
    ct: bytes = h_to_b(ct_hex)
    tag: bytes = h_to_b(tag_hex)

    comp_tag = gen_sha256(derived["k_1"], aad=aad, iv=iv, ciphertext=ct)

    if not constant_time_check(tag, comp_tag):
        raise ErrAPI(msg="invalid token", status=401)

    pt = dec_aes_cbc(derived["k_0"], iv=iv, ciphertext=ct)

    return json.loads(pt.decode("utf-8"))


print(gen_cbc_sha())
print(
    check_cbc_sha(
        "7b22616c67223a20224145532d4342432d484d41432d534841323536222c2022657870223a20313735353332313535322c202273616c74223a202232643165386437643438383338363261353330653539393261313334653565396238363737363733353737656239373830666162316331356161613134303233222c2022757365725f6964223a20223132333435222c202276223a202230227d.64a27da48c650e4dc74767a6c5f868be.026a708f33c383d4aeabc4fc609af216.2989468024679e30cbd45277e3c755611a4c80793ff82fa636fbf6662e1cf4d5"  # noqa: E501
    )
)
