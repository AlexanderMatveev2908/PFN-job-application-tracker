from email.message import EmailMessage

import aiosmtplib
from src.conf.env import env_var
from src.lib.emails.idx import gen_html_template
from src.lib.logger import clg


async def send_email(user_mail: str) -> None:
    msg = EmailMessage()
    msg["From"] = env_var.my_email
    msg["To"] = user_mail
    msg["Subject"] = "👻 ASYNC EMAIL 👻"
    msg.set_content(" Hello World " * 100)

    msg.add_alternative(await gen_html_template(), subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            username=env_var.my_email,
            password=env_var.email_pwd,
            start_tls=True,
            use_tls=False,
        )

        print("✅ email sent")
    except Exception as err:
        clg(err, ttl="err sending email")
