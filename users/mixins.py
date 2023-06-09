from django.shortcuts import redirect
from django.urls import reverse

from users.models import User


class ManagerAccessMixin:
    redirect_url = 'pages:not_found'
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == User.UserType.MANAGER:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect(reverse(self.redirect_url))
        else:
            return redirect(reverse(self.login_url))


class LoggedInUserForbiddenMixin:
    redirect_url = 'pages:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.redirect_url))
        else:
            return super().dispatch(request, *args, **kwargs)
