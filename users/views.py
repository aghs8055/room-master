from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.urls import reverse


class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            return redirect(reverse('pages:home'))
        else:
            return render(request, 'users/login.html', {'credentials': 'Invalid credentials'})
