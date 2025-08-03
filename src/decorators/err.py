class ErrAPI(Exception):
    def __init__(self, status: int, msg: str, **kwargs):
        self.status = status
        self.msg = f"💣 {msg}"
        self.data = kwargs


class ErrGen(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = f"💣 {msg}"
