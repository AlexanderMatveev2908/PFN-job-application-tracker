from functools import lru_cache
from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


HERE = Path(__file__)
ROOT = HERE.resolve().parents[4]
ROOT_ENV = ROOT / ".env"


class EnvVar(BaseSettings):
    # __ I pass also client env cause I copy paste them in every environment
    #  __ so I do not lost pieces during road

    model_config = SettingsConfigDict(
        env_file=[ROOT_ENV, ".env"],
        extra="forbid",
    )

    app_name: str = Field(..., validation_alias="APP_NAME")

    # __ client stuff
    next_public_env: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_ENV"
    )
    next_public_back_url: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_BACK_URL"
    )
    next_public_back_url_dev: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_BACK_URL_DEV"
    )
    next_public_front_url: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_FRONT_URL"
    )
    next_public_front_url_dev: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_FRONT_URL_DEV"
    )

    # __ my real env
    py_env: Literal["development", "production", "test"] = Field(
        ..., validation_alias="PY_ENV"
    )
    port: int = Field(..., validation_alias="PORT")

    # __ communication client
    front_url: str = Field(..., validation_alias="FRONT_URL")
    front_url_dev: str = Field(..., validation_alias="FRONT_URL_DEV")

    #  __ AWS
    aws_access_key: str = Field(..., validation_alias="AWS_ACCESS_KEY")
    aws_access_secret_key: str = Field(
        ..., validation_alias="AWS_ACCESS_SECRET_KEY"
    )
    aws_region_name: str = Field(..., validation_alias="AWS_REGION")
    aws_bucket_name: str = Field(..., validation_alias="AWS_BUCKET_NAME")

    # __ database — currently using Supabase as host
    db_pwd: str = Field(..., validation_alias="DB_PWD")
    db_url: str = Field(..., validation_alias="DB_URL")

    # __ test only
    secret: str | None = Field(None, validation_alias="SECRET")

    # __ email gmail provider
    my_email: str | None = Field(None, validation_alias="MY_EMAIL")
    email_pwd: str | None = Field(None, validation_alias="EMAIL_PWD")

    # __ provider brevo
    brevo_smpt_server: str = Field(..., validation_alias="BREVO_SMPT_SERVER")
    brevo_smpt_port: int = Field(..., validation_alias="BREVO_SMPT_PORT")
    brevo_smpt_user: str = Field(..., validation_alias="BREVO_SMPT_USER")
    brevo_smpt_pwd: str = Field(..., validation_alias="BREVO_SMPT_PWD")
    smpt_from: str = Field(..., validation_alias="SMPT_FROM")

    # __ redis upstash
    redis_url: str = Field(..., validation_alias="REDIS_URL")

    # __ supabase ca
    supabase_ca: str = Field(..., validation_alias="SUPABASE_CA")

    # __ tokens

    jwt_secret: str = Field(..., validation_alias="JWT_SECRET")
    jwe_public: str = Field(..., validation_alias="JWE_PUBLIC")
    jwe_private: str = Field(..., validation_alias="JWE_PRIVATE")

    master_key: str = Field(..., validation_alias="MASTER_KEY")
    pepper_key: str = Field(..., validation_alias="PEPPER_KEY")

    # __ tests CI/CD
    next_public_back_url_test: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_BACK_URL_TEST"
    )
    next_public_front_url_test: str | None = Field(
        None, validation_alias="NEXT_PUBLIC_FRONT_URL_TEST"
    )


@lru_cache
def get_env() -> EnvVar:
    return EnvVar()  # type: ignore
