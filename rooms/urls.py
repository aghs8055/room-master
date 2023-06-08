from django.urls import path

from rooms.views import (
    RequestListView,
    RequestCreateView,
    RequestDeleteView,
    RoomListView
)

app_name = 'rooms'

urlpatterns = [
    path('requests', RequestListView.as_view(), name='request_list'),
    path('create/', RequestCreateView.as_view(), name='request_create'),
    path('<int:request_id>/delete/', RequestDeleteView.as_view(), name='request_delete'),
    path('', RoomListView.as_view(), name='room_list'),
]
