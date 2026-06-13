from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='pdf_home'),

    path('pdf-to-word/', pdf_to_word, name='pdf_to_word'),

    path('word-to-pdf/', word_to_pdf, name='word_to_pdf'),

    path('merge-pdf/', merge_pdf, name='merge_pdf'),

    path('split-pdf/', split_pdf, name='split_pdf'),

    path('compress-pdf/', compress_pdf, name='compress_pdf'),

]