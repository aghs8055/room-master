from django.urls import path
from pages.views import HomeView, NotFoundView

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('not-found/', NotFoundView.as_view(), name='not_found'),
]
