import uuid

from django.conf import settings
from django.core.mail import send_mail


def get_confirmation_code():
    return uuid.uuid4().hex


def send_email(username, email, confirmation_code):
    send_mail(
        subject="Код подтверждения для YaMDB",
        from_email=settings.DEFAULT_FROM_EMAIL,
        message=(
            f'Привет, {username}! \n'
            'Ваш код подтверждения указан ниже. Перейдите по адресу'
            "'/api/v1/auth/token/' и введите код в поле "
            "'confirmation_code' для получения JWT-токена.\n"
            f'Код: {confirmation_code}'
        ),
        recipient_list=[email, ]
    )
