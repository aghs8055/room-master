from django.shortcuts import render
from django.views import View

from rooms.models import Request
from users.models import User


class RequestListView(View):
    def get(self, request):
        if request.user.user_type == User.UserType.USER:
            room_requests = Request.objects.filter(user=request.user).order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        else:
            room_requests = Request.objects.all().order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        