from functools import lru_cache
from pathlib import Path
from typing import Literal, cast
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.decorators.err import ErrAPI


HERE = Path(__file__)
ROOT = HERE.resolve().parents[4]
ROOT_ENV = ROOT / ".env"


class EnvVar(BaseSettings):
    # ? I pass also client env cause I copy paste them in every environment
    # ? so I do not lost pieces during road

    model_config = SettingsConfigDict(
        env_file=[ROOT_ENV, ".env"],
        extra="ignore",
    )

    # ? calculated during custom custom zsh scripts getting cwd lowercase
    app_name: str = Field(..., validation_alias="APP_NAME")

    # ? fly deploy tokens needed in CI/CD

    pfn_job_application_tracker__server: str = Field(
        ..., validation_alias="PFN_JOB_APPLICATION_TRACKER__SERVER"
    )
    pfn_job_application_tracker__client: str = Field(
        ..., validation_alias="PFN_JOB_APPLICATION_TRACKER__CLIENT"
    )

    # ? client stuff used also on server to not repeat same vars
    next_public_env: str = Field(..., validation_alias="NEXT_PUBLIC_ENV")
    next_public_back_url: str = Field(
        ..., validation_alias="NEXT_PUBLIC_BACK_URL"
    )
    next_public_back_url_dev: str = Field(
        ..., validation_alias="NEXT_PUBLIC_BACK_URL_DEV"
    )
    next_public_front_url: str = Field(
        ..., validation_alias="NEXT_PUBLIC_FRONT_URL"
    )
    next_public_front_url_dev: str = Field(
        ..., validation_alias="NEXT_PUBLIC_FRONT_URL_DEV"
    )

    # ? my real env
    py_env: Literal[
        "development",
        "production",
        "test",
    ] = Field(..., validation_alias="PY_ENV")
    port: int = Field(..., validation_alias="PORT")

    # ? AWS
    aws_access_key: str = Field(..., validation_alias="AWS_ACCESS_KEY")
    aws_access_secret_key: str = Field(
        ..., validation_alias="AWS_ACCESS_SECRET_KEY"
    )
    aws_region_name: str = Field(..., validation_alias="AWS_REGION")
    aws_bucket_name: str = Field(..., validation_alias="AWS_BUCKET_NAME")

    # ? database — currently using Supabase as host
    db_pwd: str = Field(..., validation_alias="DB_PWD")
    db_url: str = Field(..., validation_alias="DB_URL")

    # ? test only
    secret: str = Field(..., validation_alias="SECRET")

    # ? email gmail provider
    my_email: str = Field(..., validation_alias="MY_EMAIL")
    email_pwd: str = Field(..., validation_alias="EMAIL_PWD")

    # ? provider brevo
    brevo_smpt_server: str = Field(..., validation_alias="BREVO_SMPT_SERVER")
    brevo_smpt_port: int = Field(..., validation_alias="BREVO_SMPT_PORT")
    brevo_smpt_user: str = Field(..., validation_alias="BREVO_SMPT_USER")
    brevo_smpt_pwd: str = Field(..., validation_alias="BREVO_SMPT_PWD")
    next_public_smpt_from: str = Field(
        ..., validation_alias="NEXT_PUBLIC_SMPT_FROM"
    )
    # ? redis upstash
    redis_url: str = Field(..., validation_alias="REDIS_URL")

    # ? supabase ca
    supabase_ca: str = Field(..., validation_alias="SUPABASE_CA")

    # ? tokens

    jwt_secret: str = Field(..., validation_alias="JWT_SECRET")
    jwe_public: str = Field(..., validation_alias="JWE_PUBLIC")
    jwe_private: str = Field(..., validation_alias="JWE_PRIVATE")

    master_key: str = Field(..., validation_alias="MASTER_KEY")
    pepper_hmac_key: str = Field(..., validation_alias="PEPPER_HMAC_KEY")
    fernet_key: str = Field(..., validation_alias="FERNET_KEY")

    # ? tests CI/CD
    next_public_back_url_test: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_BACK_URL_TEST"
    )
    next_public_front_url_test: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_FRONT_URL_TEST"
    )


@lru_cache
def get_env() -> EnvVar:
    return EnvVar()  # type: ignore


@lru_cache
def get_client_url() -> str:
    env_vars = get_env()

    if env_vars.py_env == "development":
        base_url = env_vars.next_public_front_url_dev
    elif env_vars.py_env == "test":
        base_url = cast(str, env_vars.next_public_front_url_test)
    elif env_vars.py_env == "production":
        base_url = env_vars.next_public_front_url
    else:
        raise ErrAPI(msg="invalid py env", status=500)

    return cast(str, base_url)
