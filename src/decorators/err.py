class ErrAPI(Exception):
    def __init__(self, status: int, msg: str, *, opt: dict | None = None):
        self.status = status
        self.msg = msg
        self.opt = opt or {}

        super().__init__(msg)
