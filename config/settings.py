import os
from pathlib import Path

# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-secret-key')

DEBUG = False  # 🔥 IMPORTANT for production

ALLOWED_HOSTS = [
    "magic-tools-production.up.railway.app",
    ".railway.app",
]

# --------------------------------------------------
# INSTALLED APPS
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Apps
    'accounts',
    'dashboard',
    'pdf_tools',
    'image_tools',
    'ocr_tools',
    'video_tools',
    'ai_tools',
    'subscriptions',
    'payments',
    'api',
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ✔ WhiteNoise (STATIC FILE FIX)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------------
# URL CONFIG
# --------------------------------------------------
ROOT_URLCONF = 'config.urls'

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_profile',
            ],
        },
    },
]

# --------------------------------------------------
# WSGI
# --------------------------------------------------
WSGI_APPLICATION = 'config.wsgi.application'

# --------------------------------------------------
# DATABASE (⚠️ PRODUCTION WARNING)
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES (✔ FIXED FOR RAILWAY)
# --------------------------------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✔ IMPORTANT FOR WHITE NOISE
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --------------------------------------------------
# MEDIA FILES
# --------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------------------------------------
# SECURITY (PRODUCTION)
# --------------------------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --------------------------------------------------
# ENV KEYS
# --------------------------------------------------
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', None)

# --------------------------------------------------
# AUTH
# --------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# --------------------------------------------------
# DEFAULT AUTO FIELD
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
