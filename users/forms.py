from django.contrib.auth.forms import UserCreationForm, UsernameField

from users.models import User


class SignupForm(UserCreationForm):
    class Meta:
        fields = ('username',)
        model = User
        field_classes = {'username': UsernameField}
