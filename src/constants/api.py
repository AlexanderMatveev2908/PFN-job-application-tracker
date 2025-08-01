from typing import cast
from ..conf.env import env_var

whitelist: list[str] = [
    cast(
        str,
        (
            env_var.front_url_dev
            if env_var.py_env == "development"
            else env_var.front_url
        ),
    )
]
