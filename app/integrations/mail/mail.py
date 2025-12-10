from smtplib import SMTP_SSL

from redmail import EmailSender

from app.core.config import settings


class Sender(EmailSender):
    def __init__(self):
        smtp_cls = SMTP_SSL if settings.SMTP_SSL else None

        super().__init__(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_starttls=(settings.SMTP_TLS and not settings.SMTP_SSL),
            ssl=settings.SMTP_SSL,
            cls_smtp=smtp_cls,
        )

    def send(
        self,
        subject: str,
        html: str,
        mail_from: tuple[str, str] | str,
    ):
        return super().send(
            subject=subject,
            html=html,
            mail_from=mail_from,
        )


async def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"

    email = Sender()

    message = email.send(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    return {"status_code": response.status_code, "message": "Email sent successfully"}
