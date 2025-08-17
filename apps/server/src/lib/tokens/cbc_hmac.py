import json
import os
import hmac
from typing import TypedDict, cast
import uuid

from sqlalchemy import select
from src.conf.env import get_env
from src.constants.reg import REG_CBC_HMAC
from src.decorators.err import ErrAPI
from src.lib.data_structure import (
    b_to_d,
    b_to_h,
    d_to_b,
    h_to_b,
    parse_enum,
    parse_id,
)
from src.lib.algs.cbc import dec_aes_cbc, gen_aes_cbc
from src.lib.algs.hkdf import DerivedKeysCbcHmacT, derive_hkdf_cbc_hmac
from src.lib.algs.hmac import gen_hmac
from src.lib.etc import calc_exp, lt_now
from src.models.token import (
    AlgT,
    CheckTokenReturnT,
    GenTokenReturnT,
    PayloadTokenT,
    Token,
    TokenT,
)
from sqlalchemy.ext.asyncio import AsyncSession

master_key = h_to_b(get_env().master_key)


class AadT(TypedDict):
    alg: str
    token_id: str
    token_t: str
    salt: str
    user_id: str


class HdrT(
    TypedDict,
):
    token_t: TokenT


class BuildCbcHmacReturnT(TypedDict):
    token_id: str
    token: str


def build_cbc_hmac(payload: PayloadTokenT, hdr: HdrT) -> BuildCbcHmacReturnT:
    info_d: dict = {
        "alg": AlgT.AES_CBC_HMAC_SHA256.value,
        "token_t": parse_enum(hdr["token_t"]),
        "user_id": payload["user_id"],
    }

    info: bytes = d_to_b(info_d)
    salt: bytes = os.urandom(32)
    token_id = parse_id(uuid.uuid4())

    derived: DerivedKeysCbcHmacT = derive_hkdf_cbc_hmac(
        master=master_key, info=info, salt=salt
    )

    aad: bytes = d_to_b(
        {
            **info_d,
            "token_id": token_id,
            "salt": b_to_h(salt),
        }
    )

    iv, ct = gen_aes_cbc(derived["k_0"], d_to_b(cast(dict, payload)))

    aad_hex = b_to_h(aad)
    iv_hex = b_to_h(iv)
    ct_hex = b_to_h(ct)
    tag_hex: str = b_to_h(
        gen_hmac(
            derived["k_1"],
            d_to_b({"aad": aad_hex, "iv": iv_hex, "ciphertext": ct_hex}),
        )
    )

    return {
        "token": f"{aad_hex}.{iv_hex}.{ct_hex}.{tag_hex}",
        "token_id": token_id,
    }


async def gen_cbc_hmac(
    payload: PayloadTokenT, hdr: HdrT, trx: AsyncSession, reverse: bool = False
) -> GenTokenReturnT:

    result = build_cbc_hmac(payload=payload, hdr=hdr)
    client_token = result["token"]

    new_cbc_hmac = Token(
        id=result["token_id"],
        exp=calc_exp("15m", reverse),
        user_id=payload["user_id"],
        alg=AlgT.AES_CBC_HMAC_SHA256,
        **hdr,
    )
    trx.add(new_cbc_hmac)

    await trx.flush([new_cbc_hmac])
    await trx.refresh(new_cbc_hmac)

    return {
        "client_token": client_token,  # noqa: E501
        "server_token": new_cbc_hmac,
    }


def constant_time_check(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


async def check_cbc_hmac(token: str, trx: AsyncSession) -> CheckTokenReturnT:

    if not REG_CBC_HMAC.fullmatch(token):
        raise ErrAPI(msg="CBC_HMAC_INVALID_FORMAT", status=401)

    aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")

    aad_d: AadT = cast(AadT, b_to_d(h_to_b(aad_hex)))

    stm = select(Token).where(
        (Token.id == uuid.UUID(aad_d["token_id"]))
        & (Token.user_id == uuid.UUID(aad_d["user_id"]))
    )

    existing = (await trx.execute(stm)).scalar_one_or_none()

    if not existing:
        raise ErrAPI(msg="CBC_HMAC_NOT_FOUND", status=401)

    existing_d = existing.to_d()

    if lt_now(existing_d["exp"]):
        # await trx.delete(existing)
        raise ErrAPI(msg="CBC_HMAC_EXPIRED", status=401)

    info_b: bytes = d_to_b(
        {
            "alg": parse_enum(existing_d["alg"]),
            "token_t": parse_enum(existing_d["token_t"]),
            "user_id": parse_id(existing_d["user_id"]),
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

    if not constant_time_check(h_to_b(tag_hex), comp_tag):
        raise ErrAPI(msg="CBC_HMAC_INVALID", status=401)

    pt = dec_aes_cbc(
        derived["k_0"], iv=h_to_b(iv_hex), ciphertext=h_to_b(ct_hex)
    )

    return {
        "token_d": existing_d,
        "decrypted": json.loads(pt.decode("utf-8")),
    }
