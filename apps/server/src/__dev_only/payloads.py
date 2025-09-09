import datetime
import os
from typing import TypedDict, cast
import uuid

from faker import Faker
from src.lib.pwd_gen import gen_pwd
from src.models.job_application import ApplicationStatusT, JobApplicationDct

faker = Faker()


class RegisterPartPayloadT(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    terms: bool


class RegisterPayloadT(RegisterPartPayloadT):
    confirm_password: str


def get_payload_register() -> RegisterPayloadT:
    pwd = gen_pwd(enc="utf-8", n=5)
    first_name = faker.first_name()

    return {
        "first_name": first_name,
        "last_name": faker.last_name(),
        "email": f"{first_name}.{os.urandom(10).hex()}@gmail.com",
        "password": pwd,
        "confirm_password": pwd,
        "terms": True,
    }


def gen_job_appl_payload(us_id: str | uuid.UUID) -> JobApplicationDct:

    return cast(
        JobApplicationDct,
        {
            "company_name": faker.company(),
            "position_name": faker.job(),
            "applied_at": datetime.datetime.now(datetime.timezone.utc)
            .date()
            .isoformat(),
            "status": ApplicationStatusT.APPLIED.value,
            "user_id": str(us_id),
        },
    )
