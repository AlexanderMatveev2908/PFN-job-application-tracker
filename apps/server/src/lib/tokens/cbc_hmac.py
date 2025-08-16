from datetime import datetime, timedelta
import json
import os
import hmac
from typing import Any
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_d, b_to_h, d_to_b, h_to_b
from src.lib.tokens.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.tokens.hkdf import MASTERS, derive_hkdf
from src.lib.tokens.sha import gen_sha256


ALG = "AES-CBC-HMAC-SHA256"


payload: bytes = d_to_b({"id": "12345"})
payload_utf_8 = b_to_d(payload)
v = "0"


def gen_cbc_sha() -> str:

    shared_info = {
        "alg": ALG,
        "v": v,
        "user_id": payload_utf_8["id"],
    }
    info = json.dumps(shared_info).encode("utf-8")

    salt = os.urandom(16)

    derived = derive_hkdf(master=MASTERS[0], info=info, salt=salt)

    aad = json.dumps(
        {
            **shared_info,
            "salt": b_to_h(salt),
            "exp": str(
                int((datetime.now() + timedelta(minutes=15)).timestamp())
            ),
        }
    ).encode("utf-8")

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

    info = json.dumps(
        {
            "alg": ALG,
            "v": v,
            "user_id": payload_utf_8["id"],
        }
    ).encode("utf-8")

    derived = derive_hkdf(
        master=MASTERS[0],
        info=info,
        salt=h_to_b(json.loads((h_to_b(aad_hex)).decode("utf-8"))["salt"]),
    )

    aad = h_to_b(aad_hex)
    iv = h_to_b(iv_hex)
    ct = h_to_b(ct_hex)
    tag = h_to_b(tag_hex)

    comp_tag = gen_sha256(derived["k_1"], aad=aad, iv=iv, ciphertext=ct)

    if not constant_time_check(tag, comp_tag):
        raise ErrAPI(msg="invalid token", status=401)

    pt = dec_aes_cbc(derived["k_0"], iv=iv, ciphertext=ct)

    return json.loads(pt.decode("utf-8"))


print(gen_cbc_sha())
print(
    check_cbc_sha(
        "7b22616c67223a20224145532d4342432d484d41432d534841323536222c202276223a202230222c2022757365725f6964223a20223132333435222c202273616c74223a20226232666266663238656234663732373032663630366335353839303561303933222c2022657870223a202231373535333137333736227d.fe59ca1f163e44f87b982d4d8c8135c4.14541f10afe6a5a9602e93360ef958c5.751e0f47bfda47213bf6b6eb16077185f979f1ebb533d58ab10bdb12e53ef265"  # noqa: E501
    )
)
