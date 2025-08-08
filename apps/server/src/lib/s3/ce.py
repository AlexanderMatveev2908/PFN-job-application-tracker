from datetime import date, timedelta
from src.conf.aws.ce import gen_ce_session
import locale

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
# parsed_2_dec = locale.currency((arg + 20000), grouping=True)

conv = locale.localeconv()
symbol = conv["currency_symbol"]


def format_d(arg: str) -> str:
    d_iso: date = date.fromisoformat(arg)
    d_fancy = d_iso.strftime("%a %d %b")

    return d_fancy


def format_p(arg: str) -> str:
    int_part, dec_part = arg.split(".", 1) if "." in arg else (arg, "")

    rev_int = int_part[::-1]

    chunks = [
        rev_int[i : i + 3] for i in range(0, len(rev_int), 3)  # noqa: E203
    ]
    int_f = ".".join(chunks)[::-1]

    return f"{symbol}{int_f}{f".{dec_part}" if dec_part else ''}"


async def get_cost() -> None:

    async with gen_ce_session() as ce:
        start = (date.today() - timedelta(days=7)).isoformat()
        end = (date.today()).isoformat()

        res = await ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["Amazon Simple Storage Service"],
                }
            },
        )

        print("💰 bill 💸".center(12, " ").center(40, "—"))

        for x in res["ResultsByTime"]:
            d_str = x["TimePeriod"]["Start"]
            c = x["Total"]["UnblendedCost"]["Amount"]

            print(f"📅 — {format_d(d_str)} — 💸 {format_p(c)}")
