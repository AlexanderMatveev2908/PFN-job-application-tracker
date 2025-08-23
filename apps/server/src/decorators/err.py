from typing import Any


class ErrAPI(Exception):
    def __init__(self, status: int, msg: str, **kwargs: Any) -> None:
        self.status = status
        self.msg = msg
        self.data = kwargs

        super().__init__(self.msg)
