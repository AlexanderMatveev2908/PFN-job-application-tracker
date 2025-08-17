from fastapi import Request
from src.decorators.res import ResAPI


def confirm_email_ctrl(_: Request) -> ResAPI:
    return ResAPI.ok_200()
