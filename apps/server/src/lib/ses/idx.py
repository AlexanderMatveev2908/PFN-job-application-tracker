from src.conf.aws.ses import ses_session
from src.conf.email.template import gen_html_template


async def send_email() -> None:
    async with ses_session() as ses:
        await ses.send_email(
            Source="no-reply@full-stack-app.dev",
            Destination={"ToAddresses": ["matveevalexander2908@gmail.com"]},
            Message={
                "Subject": {
                    "Data": "Hi Buddy ✌🏼",
                    "Charset": "UTF-8",
                },
                "Body": {
                    "Text": {
                        "Data": " hello " * 100,
                        "Charset": "UTF-8",
                    },
                    "Html": {
                        "Data": await gen_html_template(),
                        "Charset": "UTF-8",
                    },
                },
            },
        )

        print("✅ 200")
