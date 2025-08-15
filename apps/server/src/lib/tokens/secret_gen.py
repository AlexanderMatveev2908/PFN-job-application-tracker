import os
import struct
from typing import List, TypedDict


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

    symbols = [chr(a + i) for a, b in ranges_sym for i in range(b - a + 1)]

    return {"upper": up, "lower": lw, "nums": nums, "symbols": symbols}


# print(grab_ASCI())


def gen_idx(n: int) -> int:
    MAX = 2**32
    limit = MAX - (MAX % n)

    while True:
        buf = os.urandom(4)
        v = struct.unpack("I", buf)[0]

        if v < limit:
            return v % n


print(2**32 % 12)

# print(gen_idx(100))
