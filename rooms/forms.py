from typing import Any, Dict
from datetime import datetime

from django import forms

from rooms.models import Request, Room, Reservation


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['code', 'capacity']


class RequestForm(forms.ModelForm):
    duration = forms.IntegerField(required=False)
    start_time = forms.TimeField(required=False)
    end_time = forms.TimeField(required=False)
    date = forms.DateField(required=False)

    class Meta:
        model = Request
        fields = ['duration', 'start_time', 'end_time', 'date', 'capacity']

    def save(self, user, commit=True):
        room_request = super().save(commit=False)
        room_request.user = user
        room_request.save()
        return room_request

    def clean(self):
        errors = {}

        if self.cleaned_data['duration']:
            self.cleaned_data['start_time'] = None
            self.cleaned_data['end_time'] = None
        else:
            if not self.cleaned_data['start_time']:
                errors['start_time'] = 'Start time is required.'
            if not self.cleaned_data['end_time']:
                errors['end_time'] = 'End time is required.'

        if errors:
            raise forms.ValidationError(errors)

        super().clean()


class RequestApprovalForm(forms.ModelForm):
    request = forms.IntegerField(required=True)
    force = forms.BooleanField(required=False)

    class Meta:
        model = Reservation
        fields = [
            'date',
            'start_time',
            'end_time',
            'request',
            'room',
            'force',
        ]

    def clean_request(self):
        request = Request.objects.filter(
            id=self.cleaned_data['request'],
            status=Request.Status.PENDING
        ).first()
        if request:
            return request
        else:
            raise forms.ValidationError({'request_id': 'There is no request with this ID.'})

    def clean_force(self):
        return self.cleaned_data.get('force', False)

    def get_time_diff(self, start_time, end_time):
        diff = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)
        return diff.seconds // 60

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        request = cleaned_data.get('request')

        errors = {}

        if request.date and request.date != cleaned_data.get('date'):
            errors['date'] = 'Date is not match with requested date.'

        if request.duration and request.duration != self.get_time_diff(cleaned_data.get('start_time'), cleaned_data.get('end_time')):
            errors['end_time'] = f'End time must be {request.duration} minutes after start time.'

        if not request.duration and request.start_time != cleaned_data.get('start_time'):
            errors['start_time'] = 'Start time is not match with requested start time.'

        if not request.duration and request.end_time != cleaned_data.get('end_time'):
            errors['end_time'] = 'End time is not match with requested end time.'

        if Reservation.objects.filter(room=cleaned_data.get('room'), date=cleaned_data.get('date')).exclude(start_time__gt=cleaned_data.get('end_time'), end_time__lt=cleaned_data.get('start_time')).exists():
            errors['room'] = 'This room is not available at this time.'

        if cleaned_data.get('room').capacity < request.capacity:
            errors['room'] = 'This room is too small for this request.'

        if not errors and not cleaned_data.get('force'):
            overlap_requests = Request.objects.filter(status=Request.Status.PENDING).exclude(
                id=request.id).filter(date=self.cleaned_data['date']).exclude(
                start_time__gt=self.cleaned_data['end_time'], end_time__lt=self.cleaned_data['start_time'])
            if overlap_requests.exists():
                errors['force'] = [f'User {overlap_request.user.username} also request for this time at {overlap_request.created_at.strftime("%Y-%m-%d %H:%M:%S")} with {overlap_request.capacity}.' for overlap_request in overlap_requests]

        if errors:
            raise forms.ValidationError(errors)

    def save(self, user, commit=True):
        reservation = super().save(commit=False)
        reservation.user = user
        reservation.save()
        self.cleaned_data['request'].reservation = reservation
        self.cleaned_data['request'].status = Request.Status.APPROVED
        self.cleaned_data['request'].save()
        return reservation
