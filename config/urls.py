from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),

    path('accounts/', include('accounts.urls')),

    path('pdf/', include('pdf_tools.urls')),

    path('image/', include('image_tools.urls')),

    path('ocr/', include('ocr_tools.urls')),

    path('video/', include('video_tools.urls')),

    path('ai/', include('ai_tools.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )