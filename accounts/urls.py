from django.urls import path

from .views import (
    login_view,
    register_view,
    plan_view,
    logout_view,
    profile_view,
)

urlpatterns = [
    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'plan/',
        plan_view,
        name='plan'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'profile/',
        profile_view,
        name='profile'
    ),
]