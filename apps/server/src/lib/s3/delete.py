from pathlib import Path
from src.conf.aws.s3 import gen_s3_session
from src.lib.logger import clg
from src.conf.env import env_var


async def del_asset(public_id: str) -> None:
    async with gen_s3_session() as s3:
        res = await s3.delete_object(
            Bucket=env_var.aws_bucket_name, Key=public_id
        )

        clg(res, ttl=f"🔪 deleted {public_id}")


async def del_list_assets(public_ids: list[str]) -> None:
    async with gen_s3_session() as s3:
        res = await s3.delete_objects(
            Bucket=env_var.aws_bucket_name,
            Delete={
                "Objects": [{"Key": k} for k in public_ids],
                "Quiet": False,
            },
        )

        clg(res, ttl=f"🔪 deleted {len(public_ids)} items")


async def del_folder_assets(prefix: str) -> None:
    async with gen_s3_session() as s3:
        # __ 1000 max res for req
        paginator = s3.get_paginator("list_objects_v2")
        base_path = env_var.app_name
        full_path = str(Path(base_path) / prefix)

        async for page in paginator.paginate(
            Bucket=env_var.aws_bucket_name, Prefix=full_path
        ):
            contents = page.get("Contents", [])
            if not contents:
                continue

            ids = [obj["Key"] for obj in contents]

            res = await s3.delete_objects(
                Bucket=env_var.aws_bucket_name,
                Delete={"Objects": [{"Key": id} for id in ids]},
            )

            clg(res, ttl=f"🔪 Deleted everything under '{full_path}'")
