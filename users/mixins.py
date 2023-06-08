from django.shortcuts import redirect
from django.urls import reverse

class AdminOrManagerAccessMixin:
    redirect_url = 'pages:not_found'
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.is_manager:
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
