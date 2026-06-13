from django.urls import path
from .views import history, home

urlpatterns = [
    path('', home, name='ai_home'),
    path('history/', history, name='history'),
]
