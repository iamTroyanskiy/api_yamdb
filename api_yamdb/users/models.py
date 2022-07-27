from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.enums import Roles


class User(AbstractUser):

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
        max_length=Roles.max_len(),
        choices=Roles.get_choices(),
        default=Roles.USER.name.lower()
    )
    confirmation_code = models.CharField(max_length=36, blank=True)

    USERNAME_FIELD = 'username'

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN.name.lower()

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR.name.lower()

    @property
    def is_user(self):
        return self.role == Roles.USER.name.lower()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
