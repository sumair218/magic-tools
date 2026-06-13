import os
import uuid

from django.conf import settings
from django.contrib import messages
from django.core.files import File
from django.http import FileResponse
from django.shortcuts import render

from yt_dlp import YoutubeDL

from .forms import DownloadURLForm
from .models import DownloadHistory


def _save_temp_file(content, filename):
    temp_dir = settings.MEDIA_ROOT / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / filename
    with open(file_path, 'wb') as f:
        f.write(content)
    return file_path


def _serve_file(path, filename, content_type=None):
    response = FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)
    if content_type:
        response['Content-Type'] = content_type
    return response


def home(request):
    return render(request, 'video_tools/home.html')


def _download_with_yt_dlp(url, media_type, quality):
    temp_dir = settings.MEDIA_ROOT / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    if media_type == 'audio':
        format_selector = 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best'
    else:
        if quality == 'best':
            format_selector = 'best[ext=mp4]/best'
        else:
            format_selector = f'best[height<={quality}][ext=mp4]/best[ext=mp4]/best'

    output_template = str(temp_dir / '%(id)s.%(ext)s')
    ydl_opts = {
        'outtmpl': output_template,
        'format': format_selector,
        'quiet': True,
        'nocheckcertificate': True,
        'noplaylist': True,
        'ignoreerrors': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    if not info:
        raise ValueError('Unable to download from the provided URL.')

    downloaded_filename = f"{info['id']}.{info.get('ext', 'mp4')}"
    downloaded_path = temp_dir / downloaded_filename
    return downloaded_path, downloaded_filename


def _download_view(request, tool_name, tool_description, default_media_type):
    form = DownloadURLForm(request.POST or None)
    download_url = None
    download_name = None

    if request.method == 'POST' and form.is_valid():
        url = form.cleaned_data['url']
        media_type = form.cleaned_data.get('download_type', default_media_type)
        quality = form.cleaned_data.get('video_quality', 'best')
        try:
            downloaded_path, downloaded_filename = _download_with_yt_dlp(url, media_type, quality)
            download_url = settings.MEDIA_URL.rstrip('/') + '/temp/' + downloaded_filename
            download_name = downloaded_filename

            if request.user.is_authenticated:
                try:
                    with open(downloaded_path, 'rb') as f:
                        django_file = File(f)
                        download_record = DownloadHistory(
                            user=request.user,
                            platform=tool_name,
                            url=url,
                        )
                        download_record.downloaded_file.save(downloaded_filename, django_file, save=True)
                except Exception:
                    pass
        except Exception as exc:
            messages.error(request, f'Unable to download media from the URL: {exc}')

    return render(request, 'video_tools/tool_form.html', {
        'tool_name': tool_name,
        'tool_description': tool_description,
        'form': form,
        'download_url': download_url,
        'download_name': download_name,
    })


def youtube_downloader(request):
    return _download_view(
        request,
        'YouTube Downloader',
        'Paste a YouTube URL and download the video or audio directly.',
        default_media_type='video'
    )


def social_downloader(request):
    return _download_view(
        request,
        'Social Downloader',
        'Paste a supported social media URL and download the video or audio directly.',
        default_media_type='video'
    )
