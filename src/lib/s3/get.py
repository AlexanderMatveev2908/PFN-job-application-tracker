from pathlib import Path
from typing import Mapping, TypedDict, cast
from src.conf.aws.s3 import gen_s3_session
from src.lib.logger import clg
from ...conf.env import env_var
from types_aiobotocore_s3.type_defs import (
    GetObjectOutputTypeDef,
    ObjectTypeDef,
)


async def gen_presigned_url(public_id: str) -> str:
    async with gen_s3_session() as s3:
        res = await s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": env_var.aws_bucket_name, "Key": public_id},
            ExpiresIn=60**2 * 24,
        )

        clg(res, ttl="presigned url")

        return res


class Asset(TypedDict):
    public_id: str
    content_type: str
    size: int
    metadata: Mapping[str, str]


async def save_asset(res: GetObjectOutputTypeDef, public_id: str) -> None:
    obj: Asset = {
        "public_id": public_id,
        "content_type": res.get("ContentType", ""),
        "size": res.get("ContentLength", 0),
        "metadata": (res.get("Metadata") or {}),  # OK: {} is Mapping[str, str]
    }

    file_dir = Path.cwd() / "assets"
    file_dir.mkdir(exist_ok=True)

    metadata = obj["metadata"]
    filename = metadata.get("filename", public_id)
    file_p = file_dir / filename

    stream = res["Body"]
    with file_p.open("wb") as f:
        while chunk := await stream.read(1024**2):
            f.write(chunk)


async def get_asset(public_id: str) -> None:
    async with gen_s3_session() as s3:
        res = await s3.get_object(
            Bucket=env_var.aws_bucket_name, Key=public_id
        )

        clg(res)

        await save_asset(res, public_id=public_id)


async def gen_list_assets(prefix: str = "") -> None:
    async with gen_s3_session() as s3:
        res = await s3.list_objects_v2(
            Bucket=env_var.aws_bucket_name, Prefix=prefix
        )

        contents = cast(list[ObjectTypeDef], res.get("Contents", []))
        clg(len(contents))
