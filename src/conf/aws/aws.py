from typing import TypedDict, Union
from src.conf import env


class AwsClientKwargs(TypedDict, total=False):
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    use_ssl: bool
    verify: Union[bool, str]


aws_keys: AwsClientKwargs = {
    "aws_access_key_id": env.env_var.aws_access_key,
    "aws_secret_access_key": env.env_var.aws_access_secret_key,
    "region_name": env.env_var.aws_region_name,
}
