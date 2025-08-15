import asyncio
import binascii
import json
import time
from datetime import datetime, timedelta, timezone
from typing import Any, cast
from jose import jwe

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.logger import clg

env_var = get_env()
K_ALG = "RSA-OAEP-256"
P_ALG = "A256GCM"


async def gen_jwe(**kwargs: Any) -> str:
    payload = {**kwargs}
    payload["exp"] = int(
        (datetime.now(timezone.utc) + timedelta(days=1)).timestamp()
    )

    enc_bytes: bytes = await asyncio.to_thread(
        jwe.encrypt,
        json.dumps(payload),
        binascii.unhexlify(env_var.jwe_public),
        algorithm=K_ALG,
        encryption=P_ALG,
    )

    return binascii.hexlify(enc_bytes).decode("utf-8")


async def check_jwe(hex_token: str) -> dict | None:
    jwe_bytes = binascii.unhexlify(hex_token)

    try:
        decrypted_bytes = await asyncio.to_thread(
            jwe.decrypt,
            jwe_bytes,
            binascii.unhexlify(env_var.jwe_private),
        )

        payload = json.loads(cast(bytes, decrypted_bytes).decode("utf-8"))

        if payload["exp"] < time.time():
            raise ErrAPI(msg="REFRESH_TOKEN_EXPIRED", status=401)

        return payload

    except ErrAPI:
        raise

    except Exception as err:
        clg(err, ttl="invalid token")
        raise ErrAPI(msg="REFRESH_TOKEN_INVALID", status=401)
