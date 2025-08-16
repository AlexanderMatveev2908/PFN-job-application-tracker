import asyncio
import json
import time
from typing import Any, cast
from jose import jwe

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.data_structure import h_to_b
from src.lib.etc import calc_exp
from src.lib.logger import clg

env_var = get_env()

K_ALG = "RSA-OAEP-256"
P_ALG = "A256GCM"


async def gen_jwe(**kwargs: Any) -> bytes:
    payload = {**kwargs}
    payload["exp"] = calc_exp("1d")

    enc_bytes: bytes = await asyncio.to_thread(
        jwe.encrypt,
        json.dumps(payload),
        h_to_b(env_var.jwe_public),
        algorithm=K_ALG,
        encryption=P_ALG,
    )

    return enc_bytes


async def check_jwe(token: bytes) -> dict | None:

    try:
        decrypted_bytes = await asyncio.to_thread(
            jwe.decrypt, token, h_to_b(env_var.jwe_private)
        )

        payload = json.loads(cast(bytes, decrypted_bytes).decode("utf-8"))

        if payload["exp"] < (time.time() * 1000):
            raise ErrAPI(msg="REFRESH_TOKEN_EXPIRED", status=401)

        return payload

    except ErrAPI:
        raise

    except Exception as err:
        clg(err, ttl="invalid token")
        raise ErrAPI(msg="REFRESH_TOKEN_INVALID", status=401)
