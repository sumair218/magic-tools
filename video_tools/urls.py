from django.urls import path
from .views import home, youtube_downloader, social_downloader

urlpatterns = [
    path('', home, name='video_home'),
    path('youtube-downloader/', youtube_downloader, name='youtube_downloader'),
    path('social-downloader/', social_downloader, name='social_downloader'),
]
