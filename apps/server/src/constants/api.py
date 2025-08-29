from typing import cast
from src.conf.env import get_env

env_var = get_env()

whitelist: list[str] = [
    *(
        [
            cast(
                str,
                (env_var.next_public_front_url_dev),
            )
        ]
        if env_var.py_env == "development"
        else []
    ),
    *(
        [cast(str, env_var.next_public_front_url_test)]
        if env_var.py_env == "test"
        else []
    ),
    *(
        [cast(str, env_var.next_public_front_url)]
        if env_var.py_env == "production"
        else []
    ),
]


EXPOSE_HEADERS = [
    "RateLimit-Limit",
    "RateLimit-Remaining",
    "RateLimit-Window",
    "RateLimit-Reset",
]
