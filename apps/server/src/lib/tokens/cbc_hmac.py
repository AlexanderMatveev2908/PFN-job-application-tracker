import json
import os
import hmac
from time import time
from typing import Any, TypedDict, cast
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_h, d_to_b, h_to_b
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import MASTERS, derive_hkdf
from src.lib.algs.sha import gen_sha256


class MainPayloadT(TypedDict):
    user_id: str


class PayloadT(MainPayloadT, total=False):
    opt: Any


ALG = "AES-CBC-HMAC-SHA256"


def gen_cbc_sha(payload: PayloadT) -> str:

    v: str = "0"
    shared_info = {
        "alg": ALG,
        "v": v,
        "user_id": payload["user_id"],
    }
    info: bytes = d_to_b(shared_info)

    salt: bytes = os.urandom(32)

    derived = derive_hkdf(master=MASTERS[0], info=info, salt=salt)

    aad = d_to_b(
        {
            **shared_info,
            "salt": b_to_h(salt),
            "exp": int(time()) + 15 * 60,
        }
    )

    iv, ct = gen_aes_cbc(derived["k_0"], d_to_b(cast(dict, payload)))

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


print(
    gen_cbc_sha(
        {
            "user_id": "abcdef",
        }
    )
)
print(
    check_cbc_sha(
        "7b22616c67223a20224145532d4342432d484d41432d534841323536222c2022657870223a20313735353332323836372c202273616c74223a202232663861656135373434383032313131653961306330346162303362626366653161373936306531613866336462376665313266373964353466613036396430222c2022757365725f6964223a2022616263646566222c202276223a202230227d.c5cc099e3d0017385a695c65260c32e6.e296c4a88867638fa4d15f8a9e7422fc70008255b85d37013d4c7b8cc3ad3109.4cfd81bbd90c6ec2148fc15a6fda5eec9cd63d472afa1e3725c81b7ff33eb8b1"  # noqa: E501
    )
)
