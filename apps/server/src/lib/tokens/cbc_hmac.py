import json
import os
import hmac
from time import time
from typing import Any, Literal, TypedDict, cast
import uuid

from sqlalchemy import select
from src.conf.db import db_trx
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_h, d_to_b, h_to_b, parse_id
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import DerivedKeysCbcHmacT, derive_hkdf_cbc_hmac
from src.lib.algs.hmac import gen_hmac, hmac_from_cbc
from src.models.token import AlgT, Token, TokenT


master_key = h_to_b(get_env().master_key)


class HdrT(TypedDict):
    alg: AlgT
    token_t: TokenT


class CbcHmacResT(TypedDict):
    client_token: str
    token_id: uuid.UUID


class AadT(TypedDict):
    alg: str
    token_t: str
    user_id: str
    token_id: str
    salt: str


def gen_cbc_hmac(
    payload: dict[Literal["user_id"] | str, uuid.UUID | str], hdr: HdrT
) -> CbcHmacResT:

    info_d: dict = {
        "alg": hdr["alg"].value,
        "token_t": hdr["token_t"].value,
        "user_id": parse_id(payload["user_id"]),
    }

    info: bytes = d_to_b(info_d)
    salt: bytes = os.urandom(32)

    derived: DerivedKeysCbcHmacT = derive_hkdf_cbc_hmac(
        master=master_key, info=info, salt=salt
    )
    token_id = uuid.uuid4()

    aad: bytes = d_to_b(
        {
            **info_d,
            "token_id": parse_id(token_id),
            "salt": b_to_h(salt),
        }
    )

    iv, ct = gen_aes_cbc(derived["k_0"], d_to_b(cast(dict, payload)))

    tag: bytes = gen_hmac(
        derived["k_1"],
        d_to_b(
            {"aad": b_to_h(aad), "iv": b_to_h(iv), "ciphertext": b_to_h(ct)}
        ),
    )

    return {
        "client_token": f"{b_to_h(aad)}.{b_to_h(iv)}.{b_to_h(ct)}.{b_to_h(tag)}",  # noqa: E501
        "token_id": token_id,
    }


def constant_time_check(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


async def check_cbc_hmac(token: str) -> dict[str, Any]:

    try:
        aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")
    except Exception:
        raise ErrAPI(msg="invalid token format", status=401)

    aad_d: AadT = json.loads(h_to_b(aad_hex).decode("utf-8"))

    async with db_trx() as trx:
        stm = select(Token).where(
            Token.id == uuid.UUID(aad_d["token_id"])
            and Token.token_t == TokenT(aad_d["token_t"])
        )
        existing = (await trx.execute(stm)).scalar_one_or_none()
        print(existing)
    # info_b: bytes = d_to_b(
    #     {
    #         "alg": aad_d["alg"],
    #         "token_t": aad_d["token_t"],
    #         "user_id": aad_d["user_id"],
    #     }
    # )

    # derived = derive_hkdf_cbc_hmac(
    #     master=master_key,
    #     info=info_b,
    #     salt=h_to_b(aad_d["salt"]),
    # )

    # aad: bytes = h_to_b(aad_hex)
    # iv: bytes = h_to_b(iv_hex)
    # ct: bytes = h_to_b(ct_hex)
    # tag: bytes = h_to_b(tag_hex)

    # comp_tag = hmac_from_cbc(derived["k_1"], aad=aad, iv=iv, ciphertext=ct)

    # if not constant_time_check(tag, comp_tag):
    #     raise ErrAPI(msg="invalid token", status=401)

    # pt = dec_aes_cbc(derived["k_0"], iv=iv, ciphertext=ct)

    # return json.loads(pt.decode("utf-8"))
