from typing import cast
from src.conf.env import env_var

whitelist: list[str] = [
    cast(
        str,
        (
            env_var.front_url_dev
            if env_var.py_env == "development"
            else env_var.front_url
        ),
    ),
    *([env_var.front_url_test] if env_var.front_url_test else []),
]
