"""
Django settings for healthcare_booking project.

Healthcare Booking System for Bio-Physio Consultant - Physiotherapy & Alternative Medicine Practice
"""

from pathlib import Path
import environ
import os

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Reading .env file
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-%^+*oe7ptbpyebsa=v@z!)#yx7a=zy#_7r^*em0uow#j@+vs98')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'crispy_forms',
    'crispy_tailwind',
    'corsheaders',
    'django_extensions',
    
    # Local apps
    'accounts',
    'bookings',
    'blog',
    'career',
    'contact',
    'site_settings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healthcare_booking.urls'

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
                'site_settings.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'healthcare_booking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DATABASE_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': env('DATABASE_USER', default=''),
        'PASSWORD': env('DATABASE_PASSWORD', default=''),
        'HOST': env('DATABASE_HOST', default=''),
        'PORT': env('DATABASE_PORT', default=''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',  # Custom email authentication
    'django.contrib.auth.backends.ModelBackend',  # Fallback to default
]

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

# Razorpay Configuration
# Test credentials for development
RAZORPAY_KEY_ID = env('RAZORPAY_KEY_ID', default='rzp_test_1DP5mmOlF5G5ag')
RAZORPAY_KEY_SECRET = env('RAZORPAY_KEY_SECRET', default='dIGQzxjIl2ZS6SdWrBr9IOX5')

# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@biophysioconsultant.in')

# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# PWA Settings
PWA_APP_NAME = 'Bio-Physio Consultant'
PWA_APP_DESCRIPTION = 'Healthcare booking system for physiotherapy and alternative medicine'
PWA_APP_THEME_COLOR = '#10B981'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/images/icons/icon-72x72.png',
        'sizes': '72x72',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-96x96.png',
        'sizes': '96x96',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-128x128.png',
        'sizes': '128x128',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        'sizes': '144x144',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-152x152.png',
        'sizes': '152x152',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-192x192.png',
        'sizes': '192x192',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-384x384.png',
        'sizes': '384x384',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png'
    }
]

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
