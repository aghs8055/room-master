from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Room(models.Model):
    capacity = models.PositiveIntegerField(blank=False, null=False)
    code = models.CharField(max_length=20, blank=False, null=False, unique=True)


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)


class Request(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        DENIED = 'denied', _('Denied')

    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING)
    duration = models.IntegerField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
