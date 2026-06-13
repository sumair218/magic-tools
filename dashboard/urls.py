from django.urls import path
from .views import dashboard, search

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('search/', search, name='search'),
]