from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from rooms.models import Request
from rooms.forms import RequestForm
from users.models import User


class RequestListView(View):
    def get(self, request):
        if request.user.user_type == User.UserType.USER:
            room_requests = Request.objects.filter(user=request.user).order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        else:
            room_requests = Request.objects.all().order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        
class RequestCreateView(View):
    def get(self, request):
        return render(request, 'rooms/request_create.html')
    
    def post(self, request):
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(reverse('rooms:request_list'))
        print(dict(form.errors))
        return render(request, 'rooms/request_create.html', {'errors': dict(form.errors)})
    

class RequestDeleteView(View):
    def post(self, request, request_id):
        room_request = Request.objects.filter(id=request_id, user=request.user)
        if room_request:
            room_request.delete()
            return redirect(reverse('rooms:request_list'))
        else:
            return redirect(reverse('pages:not_found'))