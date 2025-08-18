import json
import os
from typing import TypedDict, cast
import uuid

from sqlalchemy import null, select
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
from src.lib.algs.hmac import check_hmac, gen_hmac, hash_db_hmac
from src.lib.etc import calc_exp, get_now, lt_now
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
    user_id: str | uuid.UUID,
    hdr: HdrT,
    trx: AsyncSession,
    reverse: bool = False,
) -> GenTokenReturnT:

    parsed_id = user_id if isinstance(user_id, str) else str(user_id)

    result: BuildCbcHmacReturnT = build_cbc_hmac(
        payload={"user_id": parsed_id}, hdr=hdr
    )
    client_token = result["token"]

    new_cbc_hmac = Token(
        id=result["token_id"],
        exp=calc_exp("15m", reverse),
        user_id=parsed_id,
        alg=AlgT.AES_CBC_HMAC_SHA256,
        hashed=hash_db_hmac((result["token"]).encode("utf-8")),
        **hdr,
    )
    trx.add(new_cbc_hmac)

    await trx.flush([new_cbc_hmac])
    await trx.refresh(new_cbc_hmac)

    return {
        "client_token": client_token,  # noqa: E501
        "server_token": new_cbc_hmac,
    }


async def check_cbc_hmac(
    token: str, trx: AsyncSession, commit_soft_delete: bool = False
) -> CheckTokenReturnT:

    if not REG_CBC_HMAC.fullmatch(token):
        raise ErrAPI(msg="CBC_HMAC_INVALID_FORMAT", status=401)

    aad_hex, iv_hex, ct_hex, tag_hex = token.split(".")

    aad_d: AadT = cast(AadT, b_to_d(h_to_b(aad_hex)))

    stm = select(Token).where(
        (Token.id == uuid.UUID(aad_d["token_id"]))
        & (Token.user_id == uuid.UUID(aad_d["user_id"]))
        & (Token.deleted_at == null())
    )

    existing = (await trx.execute(stm)).scalar_one_or_none()

    if not existing:
        raise ErrAPI(msg="CBC_HMAC_NOT_FOUND", status=401)

    comp_hash = hash_db_hmac((token).encode("utf-8"))
    if not check_hmac(comp_hash, existing.hashed):
        raise ErrAPI(msg="CBC_HMAC_INVALID", status=401)

    if lt_now(existing.exp):
        if commit_soft_delete:
            existing.deleted_at = get_now()
            await trx.commit()
        raise ErrAPI(msg="CBC_HMAC_EXPIRED", status=401)

    info_b: bytes = d_to_b(
        {
            "alg": parse_enum(existing.alg),
            "token_t": parse_enum(existing.token_t),
            "user_id": parse_id(existing.user_id),
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
    if not check_hmac(h_to_b(tag_hex), comp_tag):
        raise ErrAPI(msg="CBC_HMAC_INVALID", status=401)

    pt = dec_aes_cbc(
        derived["k_0"], iv=h_to_b(iv_hex), ciphertext=h_to_b(ct_hex)
    )

    return {
        "token_d": existing.to_d(),
        "decrypted": json.loads(pt.decode("utf-8")),
    }
