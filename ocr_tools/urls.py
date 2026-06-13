from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='ocr_home'),

    path('image-to-text/', image_to_text, name='image_to_text'),

    path('pdf-to-text/', pdf_to_text, name='pdf_to_text'),

]