class ErrAPI(Exception):
    def __init__(self, status: int, msg: str, **kwargs):
        self.status = status
        self.msg = msg
        self.data = kwargs

        super().__init__(msg)
