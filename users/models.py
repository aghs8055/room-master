from typing import Any, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as DjangoUserManager


class User(AbstractUser):
    class UserType(models.TextChoices):
        USER = 'user', _('User')
        MANAGER = 'manager', _('Manager')

    user_type = models.CharField(max_length=7, choices=UserType.choices, default=UserType.USER)
