from django.urls import path

from rooms.views import (
    RequestListView,
    RequestCreateView,
    RequestDeleteView,
    RoomListView,
    RoomCreateView,
    RoomDeleteView,
)

app_name = 'rooms'

urlpatterns = [
    path('requests/', RequestListView.as_view(), name='request_list'),
    path('requests/create/', RequestCreateView.as_view(), name='request_create'),
    path('requests/<int:request_id>/delete/', RequestDeleteView.as_view(), name='request_delete'),
    path('', RoomListView.as_view(), name='room_list'),
    path('create/', RoomCreateView.as_view(), name='room_create'),
    path('<int:room_id>/delete/', RoomDeleteView.as_view(), name='room_delete'),
]
