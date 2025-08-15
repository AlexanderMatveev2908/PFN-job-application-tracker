import base64
import os
import struct
from typing import List, Literal, TypedDict, cast

from src.decorators.err import ErrAPI


class KeysASCI(TypedDict):
    upper: List[str]
    lower: List[str]
    nums: List[str]
    symbols: List[str]


def grab_ASCI() -> KeysASCI:
    up = [chr(65 + i) for i in range(26)]
    lw = [chr(97 + i) for i in range(26)]

    nums = [str(i) for i in range(10)]

    ranges_sym = [(33, 47), (58, 64), (91, 96), (123, 126)]
    sym = [chr(a + i) for a, b in ranges_sym for i in range(b - a + 1)]

    return {"upper": up, "lower": lw, "nums": nums, "symbols": sym}


def gen_idx(n: int) -> int:
    MAX = 2**32
    limit = MAX - (MAX % n)

    while True:
        buf = os.urandom(4)
        v = struct.unpack("I", buf)[0]

        if v < limit:
            return v % n


def shuffle(arg: str) -> str:
    lst = list(arg)

    i = len(lst) - 1

    while i:
        j = gen_idx(i + 1)

        lst[i], lst[j] = lst[j], lst[i]

        i -= 1

    return "".join(lst)


EncodingT = Literal["utf-8", "hex", "base-64"]


def gen_pwd(n: int, enc: EncodingT = "utf-8") -> str:
    d = grab_ASCI()

    pwd = ""

    for v in d.values():
        for _ in range(n):
            pwd += cast(list, v)[gen_idx(len(cast(list, v)))]

    pwd = shuffle(pwd)

    if enc == "utf-8":
        return pwd
    elif enc == "hex":
        return pwd.encode("utf-8").hex()
    elif enc == "base-64":
        return base64.b64encode(pwd.encode("utf-8")).decode("utf-8")

    raise ErrAPI(msg="invalid encoding pwd", status=500)
