import json
import os
import urllib.request
import urllib.error

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from openai import OpenAI

from .forms import AIForm
from .models import AIHistory
from video_tools.models import DownloadHistory


def _call_openrouter(prompt, api_key):
    url = 'https://openrouter.ai/api/v1/chat/completions'
    payload = json.dumps({
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 500,
        'temperature': 0.7,
        'reasoning': {'enabled': True},
    }).encode('utf-8')
    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['choices'][0]['message']['content'].strip()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode('utf-8') if hasattr(exc, 'read') else str(exc)
        raise RuntimeError(f'OpenRouter request failed: {exc.code} {exc.reason} {error_body}')


def _get_ai_response(prompt):
    openrouter_key = os.getenv('OPENROUTER_API_KEY', getattr(settings, 'OPENROUTER_API_KEY', None))
    if openrouter_key:
        return _call_openrouter(prompt, openrouter_key)

    openai_key = os.getenv('OPENAI_API_KEY', getattr(settings, 'OPENAI_API_KEY', None))
    if openai_key:
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    return None


@login_required(login_url='login')
def home(request):
    form = AIForm(request.POST or None)
    ai_response = None
    recent_history = AIHistory.objects.filter(user=request.user).order_by('-created_at')[:5]

    if request.method == 'POST' and form.is_valid():
        prompt = form.cleaned_data['prompt']
        ai_response = _get_ai_response(prompt)

        if ai_response is None:
            messages.error(
                request,
                'AI service is not configured. Set OPENROUTER_API_KEY or OPENAI_API_KEY in your environment.'
            )
        else:
            try:
                AIHistory.objects.create(
                    user=request.user,
                    prompt=prompt,
                    response=ai_response,
                )
                recent_history = AIHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
            except Exception as exc:
                messages.error(request, f'AI request failed: {exc}')

    return render(request, 'ai_tools/home.html', {
        'form': form,
        'ai_response': ai_response,
        'recent_history': recent_history,
    })


@login_required(login_url='login')
def history(request):
    ai_history = AIHistory.objects.filter(user=request.user).order_by('-created_at')
    video_history = DownloadHistory.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'ai_tools/history.html', {
        'ai_history': ai_history,
        'video_history': video_history,
    })
