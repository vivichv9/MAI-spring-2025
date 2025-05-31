import smtplib
from email.message import EmailMessage
from starlette.templating import Jinja2Templates
from celery import shared_task

from core.settings import settings


@shared_task
def send_confirmation_email(to_email: str, token: str) -> None:
    confirmation_url = f"{settings.frontend_url}/auth/register_confirm?token={token}"

    templates = Jinja2Templates(directory=str(settings.templates_dir))
    template = templates.get_template(name="confirmation_email.html")
    html_content = template.render(confirmation_url=confirmation_url)

    message = EmailMessage()
    message.add_alternative(html_content, subtype="html")
    message["From"] = settings.email_settings.email_username
    message["To"] = to_email
    message["Subject"] = "Подтверждение регистрации"

    with smtplib.SMTP_SSL(host=settings.email_settings.email_host, port=settings.email_settings.email_port) as smtp:
        smtp.login(
            user=settings.email_settings.email_username,
            password=settings.email_settings.email_password.get_secret_value(),
        )
        smtp.send_message(msg=message)