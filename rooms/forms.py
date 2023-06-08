from typing import Any, Dict
from django import forms

from rooms.models import Request, Room


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
        fields = ['duration', 'start_time', 'end_time', 'date']

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
                