from pathlib import Path
from src.conf.aws.s3 import gen_s3_session
from src.lib.logger import clg
from ...conf.env import env_var


async def gen_presigned_url(public_id: str) -> str:
    async with gen_s3_session() as s3:
        return await s3.generate_presigned_url(  # type: ignore
            ClientMethod="get_object",
            Params={"Bucket": env_var.aws_bucket_name, "Key": public_id},
            ExpiresIn=60**2 * 24,
        )


async def save_asset(res: dict, public_id: str) -> None:
    obj = {
        "public_id": public_id,
        "content_type": res.get("ContentType", ""),
        "size": res.get("ContentLength", 0),
        "metadata": res.get("Metadata", {}),
    }

    # ext = mimetypes.guess_extension(obj["content_type"]) or ""
    # body_b = await res["Body"].read()
    file_dir = Path.cwd() / "assets"
    file_dir.mkdir(exist_ok=True)
    file_p = file_dir / obj["metadata"]["filename"]
    # file_p.write_bytes(body_b)

    stream = res["Body"]
    with file_p.open("wb") as f:
        while chunk := await stream.read(1024**2):
            f.write(chunk)


async def get_asset(public_id: str) -> None:
    async with gen_s3_session() as s3:
        res = await s3.get_object(  # type: ignore
            Bucket=env_var.aws_bucket_name, Key=public_id
        )

        clg(res)


async def gen_list_assets(prefix: str = "") -> None:
    async with gen_s3_session() as s3:
        res = await s3.list_objects_v2(  # type: ignore
            Bucket=env_var.aws_bucket_name, Prefix=prefix
        )

        clg(len(res["Contents"]))
