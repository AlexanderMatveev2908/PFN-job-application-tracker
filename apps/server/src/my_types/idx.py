from typing import Literal

ParamWindowTime = Literal["15m", "30m", "1h", "1d"]

MAPPER_WINDOW_TIME: dict[ParamWindowTime, int] = {
    "15m": 60 * 15,
    "30m": 60 * 30,
    "1h": 60**2,
    "1d": 24 * 60**2,
}
