import datetime
from src.conf.aws.ce import gen_ce_session
from src.lib.logger import clg


async def get_cost() -> None:

    async with gen_ce_session() as ce:
        start = (datetime.date.today()).isoformat()
        end = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()

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

        clg(res, ttl="bill")
