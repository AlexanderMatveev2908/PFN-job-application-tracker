from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.test.middleware.check_user import User, check_user


async def get_test(_: Request, user: User = Depends(check_user)) -> ResAPI:

    return ResAPI.ok_201(data=user)
