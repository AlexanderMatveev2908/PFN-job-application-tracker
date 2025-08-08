from typing import Callable, cast
from uuid import UUID
from fastapi import Request

from src.decorators.err import ErrAPI
from src.lib.logger import clg


def check_id_mdw(k: str) -> Callable[[Request], UUID]:
    def check_uuid(req: Request) -> UUID:
        id = req.path_params.get(k)

        if not k:
            raise ErrAPI(msg=f"{k} missing in params", status=400)

        try:
            parsed = UUID(id, version=4)

            return cast(UUID, parsed)
        except Exception as err:
            clg(err, ttl=f"invalid uuid4 => {id}")
            raise ErrAPI(msg="Invalid uuid4 provided", status=400)

    return check_uuid
