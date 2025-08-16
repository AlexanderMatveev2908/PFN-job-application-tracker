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


def gen_cbc_sha(payload: PayloadT, v: str) -> str:

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
        },
        v="0",
    )
)
print(
    check_cbc_sha(
        "7b22616c67223a224145532d4342432d484d41432d534841323536222c22657870223a313735353332333538382c2273616c74223a2235303634343236343730346531646361376362393066306233333339396334656335376131636134373564393036356662333333656163633863313766346666222c22757365725f6964223a22616263646566222c2276223a2230227d.8f568fb425d6869a626c4ecf0c070d9e.6b47bc674ee4a8477287309b31bd28f7b6a927ba58750b34637bc887c6f56d46.ac804a35076d39dfdb9bcb1acba956a986c90b601ee0eae2fa0240f074dcd291"  # noqa: E501
    )
)
