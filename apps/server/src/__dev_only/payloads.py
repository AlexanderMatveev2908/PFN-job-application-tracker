import datetime
import os
import random
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


status_str = [x.value for x in ApplicationStatusT]


def gen_payload_application_client() -> dict:
    return {
        "company_name": faker.company(),
        "position_name": faker.job(),
        "applied_at": datetime.datetime.now(datetime.timezone.utc)
        .date()
        .isoformat(),
        "status": random.choice(status_str),
        "notes": gen_lorem(4),
    }


def gen_job_appl_payload_server(us_id: str | uuid.UUID) -> JobApplicationDct:

    return cast(
        JobApplicationDct,
        {
            **gen_payload_application_client(),
            "user_id": str(us_id),
        },
    )


def gen_lorem(n: int | None = None) -> str:
    return (
        "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Exercitationem perferendis nostrum, sapiente dicta praesentium neque ratione rem facilis. Alias quos libero vel iusto quam in, recusandae accusamus cupiditate fugiat nam."  # noqa: E501
        * (n or 1)
    )
