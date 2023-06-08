from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse

from users.forms import SignupForm
from users.mixins import LoggedInUserForbiddenMixin


class LoginView(LoggedInUserForbiddenMixin, View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(self.get_redirect_url())
        else:
            return render(request, 'users/login.html', {'credentials': 'Invalid credentials'})
        
    def get_redirect_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('pages:home')
        

class SignupView(LoggedInUserForbiddenMixin, View):
    def get(self, request):
        return render(request, 'users/signup.html')
    
    def post(self, request):
        user_form = SignupForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('users:login'))
        else:
            print(request.POST)
            print(dict(user_form.errors))
            return render(request, 'users/signup.html', {'errors': dict(user_form.errors)})
        

class LogoutView(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse('pages:home'))
