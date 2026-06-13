import os
import uuid

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render

from PIL import Image

from .forms import ImageUploadForm, ResizeImageForm


def _save_temp_file(uploaded_file):
    temp_dir = settings.MEDIA_ROOT / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
    file_path = temp_dir / filename
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path


def _serve_file(path, filename, content_type=None):
    response = FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)
    if content_type:
        response['Content-Type'] = content_type
    return response


def home(request):
    return render(request, 'image_tools/home.html')


def jpg_to_png(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        image_path = _save_temp_file(form.cleaned_data['image_file'])
        try:
            with Image.open(image_path) as image:
                output_path = settings.MEDIA_ROOT / 'temp' / f"{uuid.uuid4().hex}.png"
                image.save(output_path, format='PNG')
                download_name = f"{os.path.splitext(form.cleaned_data['image_file'].name)[0]}.png"
                return _serve_file(output_path, download_name, content_type='image/png')
        except Exception:
            messages.error(request, 'Unable to convert the uploaded image to PNG.')

    return render(request, 'image_tools/tool_form.html', {
        'tool_name': 'JPG to PNG',
        'tool_description': 'Upload a JPEG or JPG image and convert it to PNG format.',
        'form': form,
    })


def png_to_jpg(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        image_path = _save_temp_file(form.cleaned_data['image_file'])
        try:
            with Image.open(image_path) as image:
                if image.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                else:
                    image = image.convert('RGB')

                output_path = settings.MEDIA_ROOT / 'temp' / f"{uuid.uuid4().hex}.jpg"
                image.save(output_path, format='JPEG', quality=90)
                download_name = f"{os.path.splitext(form.cleaned_data['image_file'].name)[0]}.jpg"
                return _serve_file(output_path, download_name, content_type='image/jpeg')
        except Exception:
            messages.error(request, 'Unable to convert the uploaded image to JPG.')

    return render(request, 'image_tools/tool_form.html', {
        'tool_name': 'PNG to JPG',
        'tool_description': 'Upload a PNG image and convert it to JPG format.',
        'form': form,
    })


def resize_image(request):
    form = ResizeImageForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        width = form.cleaned_data.get('width')
        height = form.cleaned_data.get('height')

        if not width and not height:
            messages.error(request, 'Please specify at least a width or a height.')
        else:
            image_path = _save_temp_file(form.cleaned_data['image_file'])
            try:
                with Image.open(image_path) as image:
                    original_width, original_height = image.size

                    if width and not height:
                        height = round((width / original_width) * original_height)
                    elif height and not width:
                        width = round((height / original_height) * original_width)

                    resized = image.resize((width, height), Image.LANCZOS)

                    output_ext = image.format.lower() if image.format else 'png'
                    output_name = f"{uuid.uuid4().hex}.{output_ext}"
                    output_path = settings.MEDIA_ROOT / 'temp' / output_name

                    if output_ext in ('jpg', 'jpeg') and resized.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', resized.size, (255, 255, 255))
                        background.paste(resized, mask=resized.split()[-1])
                        resized = background
                        resized.save(output_path, format='JPEG', quality=90)
                    else:
                        resized.save(output_path, format=image.format or 'PNG')

                    download_name = f"{os.path.splitext(form.cleaned_data['image_file'].name)[0]}_resized.{output_ext}"
                    return _serve_file(output_path, download_name, content_type=f'image/{output_ext}')
            except Exception:
                messages.error(request, 'Unable to resize the uploaded image.')

    return render(request, 'image_tools/tool_form.html', {
        'tool_name': 'Resize Image',
        'tool_description': 'Upload an image and resize it by width, height, or both.',
        'form': form,
    })


def compress_image(request):
    from .forms import CompressImageForm

    form = CompressImageForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        image_path = _save_temp_file(form.cleaned_data['image_file'])
        quality = form.cleaned_data['quality']

        try:
            with Image.open(image_path) as image:
                output_ext = image.format.lower() if image.format else 'jpg'
                output_name = f"{uuid.uuid4().hex}.{output_ext}"
                output_path = settings.MEDIA_ROOT / 'temp' / output_name

                save_options = {
                    'optimize': True,
                }

                if output_ext in ('jpg', 'jpeg'):
                    if image.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[-1])
                        image = background
                    else:
                        image = image.convert('RGB')

                    save_options['quality'] = quality
                    save_options['progressive'] = True
                    image.save(output_path, format='JPEG', **save_options)
                elif output_ext == 'png':
                    image.save(output_path, format='PNG', compress_level=max(0, min(9, 9 - (quality // 10))), **save_options)
                else:
                    image.save(output_path, format=image.format or 'JPEG', quality=quality, **save_options)

                download_name = f"{os.path.splitext(form.cleaned_data['image_file'].name)[0]}_compressed.{output_ext}"
                return _serve_file(output_path, download_name, content_type=f'image/{output_ext}')
        except Exception:
            messages.error(request, 'Unable to compress the uploaded image.')

    return render(request, 'image_tools/tool_form.html', {
        'tool_name': 'Compress Image',
        'tool_description': 'Upload an image and reduce its file size while keeping quality acceptable.',
        'form': form,
    })
