from typing import Any, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('user_type', User.UserType.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class UserType(models.TextChoices):
        USER = 'user', _('User')
        ADMIN = 'admin', _('Admin')
        MANAGER = 'manager', _('Manager')

    user_type = models.CharField(max_length=7, choices=UserType.choices, default=UserType.USER)
    
    objects = UserManager()
