from django.urls import path

from rooms.views import RequestListView

app_name = 'rooms'

urlpatterns = [
    path('', RequestListView.as_view(), name='request_list'),
]
