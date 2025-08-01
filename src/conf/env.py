from pydantic import Field
from pydantic_settings import BaseSettings


class EnvVar(BaseSettings):
    # __ I pass also client env cause I copy paste them in every environment
    #  __ so I do not lost pieces during road

    # __ client stuff
    next_public_env: str | None = Field(None, alias="NEXT_PUBLIC_ENV")
    next_public_back_url: str | None = Field(
        None, alias="NEXT_PUBLIC_BACK_URL"
    )
    next_public_back_url_dev: str | None = Field(
        None, alias="NEXT_PUBLIC_BACK_URL_DEV"
    )
    next_public_front_url: str | None = Field(
        None, alias="NEXT_PUBLIC_FRONT_URL"
    )
    next_public_front_url_dev: str | None = Field(
        None, alias="NEXT_PUBLIC_FRONT_URL_DEV"
    )

    # __ my real env
    py_env: str = Field(..., alias="PY_ENV")
    port: int = Field(..., alias="PORT")

    # __ communication client
    front_url: str | None = Field(None, alias="FRONT_URL")
    front_url_dev: str | None = Field(None, alias="FRONT_URL_DEV")

    # __ test only
    secret: str = Field(..., alias="SECRET")

    class Config:
        env_file = ".env"
        extra = "forbid"


env_var = EnvVar()  # type: ignore
