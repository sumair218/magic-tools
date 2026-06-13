from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='image_home'),

    path('jpg-to-png/', jpg_to_png, name='jpg_to_png'),

    path('png-to-jpg/', png_to_jpg, name='png_to_jpg'),

    path('resize/', resize_image, name='resize'),

    path('compress/', compress_image, name='compress_image'),

]