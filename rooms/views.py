from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from rooms.models import Request, Room, Reservation
from rooms.forms import RequestForm, RoomForm
from users.models import User
from users.mixins import AdminOrManagerAccessMixin


def get_filtered_reservations(reservations, filter):
    today = timezone.now()
    start_week = today - timezone.timedelta(days=today.weekday())
    end_week = start_week + timezone.timedelta(days=7)
    queries = {
        'all': reservations,
        'today': reservations.filter(date=timezone.now()),
        'this-week': reservations.filter(date__range=[start_week, end_week]),
        'this-month': reservations.filter(date__month=today.month),
        'last-7-days': reservations.filter(date__range=[today - timezone.timedelta(days=7), today]),
        'next-7-days': reservations.filter(date__range=[today, today + timezone.timedelta(days=7)]),
        'last-30-days': reservations.filter(date__range=[today - timezone.timedelta(days=30), today]),
        'next-30-days': reservations.filter(date__range=[today, today + timezone.timedelta(days=30)]),
    }
    if filter in queries:
        return queries[filter]
    return queries['all']


class RequestListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.user_type == User.UserType.USER:
            room_requests = Request.objects.filter(user=request.user).order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})
        else:
            room_requests = Request.objects.all().order_by('-created_at')
            return render(request, 'rooms/request_list.html', {'room_requests': room_requests})


class RequestCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'rooms/request_form.html')

    def post(self, request):
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(reverse('rooms:request_list'))
        print(dict(form.errors))
        return render(request, 'rooms/request_form.html', {'errors': dict(form.errors)})


class RequestDeleteView(AdminOrManagerAccessMixin, View):
    def post(self, request, request_id):
        room_request = Request.objects.filter(id=request_id, user=request.user)
        if room_request:
            room_request.delete()
            return redirect(reverse('rooms:request_list'))
        else:
            return redirect(reverse('pages:not_found'))


class RequestEditView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        room_request = Request.objects.filter(
            user=request.user,
            id=request_id,
            status=Request.Status.PENDING
        )
        if room_request:
            return render(request, 'rooms/request_form.html', {'room_request': room_request[0]})
        else:
            return redirect(reverse('pages:not_found'))

    def post(self, request, request_id):
        room_request = Request.objects.filter(
            user=request.user,
            id=request_id,
            status=Request.Status.PENDING
        )
        if room_request:
            form = RequestForm(request.POST, instance=room_request[0])
            if form.is_valid():
                form.save(user=request.user)
                return redirect(reverse('rooms:request_list'))
            return render(request, 'rooms/request_form.html', {'errors': dict(form.errors)})
        else:
            return redirect(reverse('pages:not_found'))


class RoomListView(LoginRequiredMixin, View):
    def get(self, request):
        rooms = Room.objects.all().order_by('code')
        return render(request, 'rooms/room_list.html', {'rooms': rooms})


class RoomCreateView(AdminOrManagerAccessMixin, View):
    def get(self, request):
        return render(request, 'rooms/room_form.html')

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rooms:room_list'))
        return render(request, 'rooms/room_form.html', {'errors': dict(form.errors)})


class RoomDeleteView(AdminOrManagerAccessMixin, View):
    def post(self, request, room_id):
        room = Room.objects.filter(id=room_id)
        if room:
            room.delete()
            return redirect(reverse('rooms:room_list'))
        else:
            return redirect(reverse('pages:not_found'))


class RoomEditView(AdminOrManagerAccessMixin, View):
    def get(self, request, room_id):
        room = Room.objects.filter(id=room_id)
        if room:
            return render(request, 'rooms/room_form.html', {'room': room[0]})
        else:
            return redirect(reverse('pages:not_found'))

    def post(self, request, room_id):
        room = Room.objects.filter(id=room_id)
        if room:
            form = RoomForm(request.POST, instance=room[0])
            if form.is_valid():
                form.save()
                return redirect(reverse('rooms:room_list'))
            return render(request, 'rooms/room_form.html', {'errors': dict(form.errors)})
        else:
            return redirect(reverse('pages:not_found'))


class ReservationListView(AdminOrManagerAccessMixin, View):
    def get(self, request):
        reservations = Reservation.objects.all().order_by('-date')
        reservations = get_filtered_reservations(reservations, request.GET.get('filter'))
        return render(request, 'rooms/reservation_list.html', {'reservations': reservations})


class RoomReservationList(AdminOrManagerAccessMixin, View):
    def get(self, request, room_id):
        reservations = Reservation.objects.filter(room_id=room_id)
        reservations = get_filtered_reservations(reservations, request.GET.get('filter'))
        return render(request, 'rooms/reservation_list.html', {'reservations': reservations})


class ReservationDetailView(LoginRequiredMixin, View):
    def get(self, request, reservation_id):
        if request.user.user_type == User.UserType.USER:
            reservation = Reservation.objects.filter(id=reservation_id, user=request.user)
        else:
            reservation = Reservation.objects.filter(id=reservation_id)
        if reservation:
            return render(request, 'rooms/reservation_detail.html', {'reservation': reservation[0]})
        else:
            return redirect(reverse('pages:not_found'))
