from django.shortcuts import redirect, render


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def search(request):
    query = request.GET.get('q', '').strip().lower()

    if not query:
        return redirect('dashboard')

    tool_routes = {
        'pdf': 'pdf_home',
        'word': 'pdf_home',
        'image': 'image_home',
        'jpg': 'image_home',
        'png': 'image_home',
        'ocr': 'ocr_home',
        'text': 'ocr_home',
        'video': 'video_home',
        'youtube': 'video_home',
        'social': 'social_downloader',
        'ai': 'ai_home',
        'chat': 'ai_home',
        'history': 'history',
    }

    for keyword, route_name in tool_routes.items():
        if keyword in query:
            return redirect(route_name)

    return redirect('dashboard')
