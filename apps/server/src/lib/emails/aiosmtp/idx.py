from email.message import EmailMessage

import aiosmtplib
from src.conf.env import get_env
from src.lib.emails.idx import gen_html_template
from src.lib.logger import clg
from src.models.user import User

env_var = get_env()


async def send_email(user: User, subj: str, callback_url: str) -> None:
    msg = EmailMessage()
    msg["From"] = (env_var.smpt_from,)
    msg["To"] = (user.email,)
    msg["Subject"] = (subj,)
    msg.set_content(
        f"Hi {user.first_name}\n\n",
        "Click the link below to be redirected"
        " to our verification page 🔒\n\n",
        f"{callback_url}",
    )

    msg.add_alternative(
        await gen_html_template(first_name=user.first_name, url=callback_url),
        subtype="html",
    )

    try:
        await aiosmtplib.send(
            msg,
            hostname=env_var.brevo_smpt_server,
            port=env_var.brevo_smpt_port,
            username=env_var.brevo_smpt_user,
            password=env_var.brevo_smpt_pwd,
            start_tls=True,
            use_tls=False,
        )

        print("✅ smtp")
    except Exception as err:
        clg(err, ttl="err sending email")


# async def send_email_gmail(user_mail: str) -> None:
#     msg = EmailMessage()
#     msg["From"] = env_var.my_email
#     msg["To"] = user_mail
#     msg["Subject"] = "👻 ASYNC EMAIL 👻"
#     msg.set_content(" Hello World " * 100)

#     msg.add_alternative(await gen_html_template(), subtype="html")

#     try:
#         await aiosmtplib.send(
#             msg,
#             hostname="smtp.gmail.com",
#             port=587,
#             username=env_var.my_email,
#             password=env_var.email_pwd,
#             start_tls=True,
#             use_tls=False,
#         )

#         print("✅ smtp")
#     except Exception as err:
#         clg(err, ttl="err sending email")
