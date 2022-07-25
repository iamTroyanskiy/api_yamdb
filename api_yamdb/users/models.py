from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLES = (
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    )

    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message=(
            "Username должен содержать только буквы, "
            "цифры и символы: '@', '.', '+', '-', '_'"
        )
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[username_validator, ]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=14,
        choices=USER_ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(max_length=36, blank=True)

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
