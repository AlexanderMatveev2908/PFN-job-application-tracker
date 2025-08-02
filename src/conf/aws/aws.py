from src.conf import env


aws_keys = {
    "aws_access_key_id": env.env_var.aws_access_key,
    "aws_secret_access_key": env.env_var.aws_access_secret_key,
    "region_name": env.env_var.aws_region_name,
}
