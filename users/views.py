from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse

from users.forms import SignupForm


class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('pages:home'))
        else:
            return render(request, 'users/login.html', {'credentials': 'Invalid credentials'})
        

class SignupView(View):
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
