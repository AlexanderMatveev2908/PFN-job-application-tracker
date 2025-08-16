import json
import os
import hmac
from typing import Any, TypedDict, cast
import uuid

from sqlalchemy import select
from src.conf.db import db_trx
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.data_structure import b_to_h, d_to_b, h_to_b, parse_enum, parse_id
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import DerivedKeysCbcHmacT, derive_hkdf_cbc_hmac
from src.lib.algs.hmac import gen_hmac
from src.lib.etc import calc_exp, lt_now
from src.models.token import AlgT, PayloadTokenT, Token, TokenT
from sqlalchemy.ext.asyncio import AsyncSession

master_key = h_to_b(get_env().master_key)


class HdrT(TypedDict):
    alg: AlgT
    token_t: TokenT


class CbcHmacResT(TypedDict):
    client_token: str
    server_token: Token


class AadT(TypedDict):
    alg: str
    token_id: str
    token_t: str
    salt: str
    user_id: str


async def gen_cbc_hmac(
    payload: PayloadTokenT, hdr: HdrT, trx: AsyncSession
) -> CbcHmacResT:

    info_d: dict = {
        "alg": parse_enum(hdr["alg"]),
        "token_t": parse_enum(hdr["token_t"]),
        "user_id": parse_id(payload["user_id"]),
    }

    info: bytes = d_to_b(info_d)
    salt: bytes = os.urandom(32)

    derived: DerivedKeysCbcHmacT = derive_hkdf_cbc_hmac(
        master=master_key, info=info, salt=salt
    )
    token_id = parse_id(uuid.uuid4())

    aad: bytes = d_to_b(
        {
            **info_d,
            "token_id": token_id,
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

    new_cbc_hmac = Token(
        id=token_id,
        exp=calc_exp("15m"),
        user_id=payload["user_id"],
        **hdr,
    )
    trx.add(new_cbc_hmac)

    await trx.flush([new_cbc_hmac])
    await trx.refresh(new_cbc_hmac)

    return {
        "client_token": f"{b_to_h(aad)}.{b_to_h(iv)}.{b_to_h(ct)}.{b_to_h(tag)}",  # noqa: E501
        "server_token": new_cbc_hmac,
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
        existing = cast(
            Token, (await trx.execute(stm)).scalar_one_or_none()
        ).to_d()

        if lt_now(existing["exp"]):
            raise ErrAPI(msg="token expired", status=401)

        info_b: bytes = d_to_b(
            {
                "alg": parse_enum(existing["alg"]),
                "token_t": parse_enum(existing["token_t"]),
                "user_id": parse_id(existing["user_id"]),
            }
        )

        derived = derive_hkdf_cbc_hmac(
            master=h_to_b(get_env().master_key),
            info=info_b,
            salt=h_to_b(aad_d["salt"]),
        )

        comp_tag = gen_hmac(
            derived["k_1"],
            d_to_b(
                {"aad": aad_hex, "iv": iv_hex, "ciphertext": ct_hex},
            ),
        )

        pt = dec_aes_cbc(
            derived["k_0"], iv=h_to_b(iv_hex), ciphertext=h_to_b(ct_hex)
        )

        if not constant_time_check(h_to_b(tag_hex), comp_tag):
            raise ErrAPI(msg="invalid token", status=401)

        return json.loads(pt.decode("utf-8"))
