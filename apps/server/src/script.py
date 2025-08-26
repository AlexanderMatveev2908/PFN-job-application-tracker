from src.lib.etc import grab


print("script worked ✅")


d = {
    "level_a": {
        "level_b": {"level_c": {"level_d": {"val": "i do not want it"}}}
    },
    "val": "what i want",
}


print(grab(d, "val", exclude_parents=["level_a"]))
