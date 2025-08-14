from typing import TypedDict, Union, cast
from src.conf.env import get_env


class AwsClientKwargs(TypedDict, total=False):
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    use_ssl: bool
    verify: Union[bool, str]


env_var = get_env()

aws_keys: AwsClientKwargs = {
    "aws_access_key_id": cast(str, env_var.aws_access_key),
    "aws_secret_access_key": cast(str, env_var.aws_access_secret_key),
    "region_name": cast(str, env_var.aws_region_name),
}
