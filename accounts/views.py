from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from .forms import CustomPasswordChangeForm, LoginForm, ProfileForm, RegisterForm
from .models import Profile


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! You are now on the dashboard.")
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')

        messages.error(request, "Login failed. Please check your username and password.")

    return render(
        request,
        'accounts/login.html',
        {'form': form, 'next': request.POST.get('next', request.GET.get('next', ''))}
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            Profile.objects.get_or_create(user=user)
            login(request, user)

            messages.success(
                request,
                f"Welcome, {user.username}! Your account is ready. Choose a plan next."
            )

            return redirect('plan')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


@login_required(login_url='login')
def plan_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        plan = request.POST.get('plan')
        if plan == 'premium':
            profile.is_premium = True
            messages.success(request, 'Premium plan selected. Welcome to the dashboard!')
        else:
            profile.is_premium = False
            messages.success(request, 'Free plan selected. You can upgrade anytime.')

        profile.save()
        return redirect('dashboard')

    return render(request, 'accounts/billing.html', {
        'profile': profile,
    })


def logout_view(request):
    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )

    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile)
    password_form = CustomPasswordChangeForm(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_image':
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile image updated successfully.')
                return redirect('profile')
        elif action == 'change_password':
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please fix the password form errors.')

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_form': profile_form,
            'password_form': password_form,
            'profile': profile,
        }
    )