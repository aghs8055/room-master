from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from rooms.models import Request, Room
from rooms.forms import RequestForm, RoomForm
from users.models import User
from users.mixins import AdminOrManagerAccessMixin


class RequestListView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        if request.user.user_type == User.UserType.USER:
            room_requests = Request.objects.filter(user=request.user).order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        else:
            room_requests = Request.objects.all().order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        
class RequestCreateView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        return render(request, 'rooms/request_create.html')
    
    def post(self, request):
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(reverse('rooms:request_list'))
        print(dict(form.errors))
        return render(request, 'rooms/request_create.html', {'errors': dict(form.errors)})
    

class RequestDeleteView(AdminOrManagerAccessMixin, View):
    def post(self, request, request_id):
        room_request = Request.objects.filter(id=request_id, user=request.user)
        if room_request:
            room_request.delete()
            return redirect(reverse('rooms:request_list'))
        else:
            return redirect(reverse('pages:not_found'))
        

class RoomListView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'rooms/room_list.html', {'rooms': rooms})
    

class RoomCreateView(AdminOrManagerAccessMixin, View):
    def get(self, request):
        return render(request, 'rooms/room_create.html')
    
    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rooms:room_list'))
        return render(request, 'rooms/room_create.html', {'errors': dict(form.errors)})
    

class RoomDeleteView(AdminOrManagerAccessMixin, View):
    def post(self, request, room_id):
        room = Room.objects.filter(id=room_id)
        if room:
            room.delete()
            return redirect(reverse('rooms:room_list'))
        else:
            return redirect(reverse('pages:not_found'))
