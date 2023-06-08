from django.urls import path

from rooms.views import RequestListView, RequestCreateView

app_name = 'rooms'

urlpatterns = [
    path('', RequestListView.as_view(), name='request_list'),
    path('create/', RequestCreateView.as_view(), name='request_create'),
]
