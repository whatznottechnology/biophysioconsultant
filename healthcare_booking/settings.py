"""
Django settings for healthcare_booking project.

Healthcare Booking System for Bio-Physio Consultant - Physiotherapy & Alternative Medicine Practice
"""

from pathlib import Path
import environ
import os
from django.templatetags.static import static
from django.urls import reverse_lazy

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Helper function for logo
def get_site_logo_or_fallback(request):
    """Get site logo from settings or return fallback logo"""
    try:
        from site_settings.models import SiteSettings
        settings = SiteSettings.get_settings()
        if settings.site_logo:
            return request.build_absolute_uri(settings.site_logo.url)
    except:
        pass
    return static("images/loogoo.png")

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
    'unfold',  # Django Unfold - before django.contrib.admin
    'unfold.contrib.filters',  # optional, if special filters are used
    'unfold.contrib.forms',  # optional, if special form elements are used
    
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
# AUTH_USER_MODEL = 'accounts.User'

# Authentication Backends
# AUTHENTICATION_BACKENDS = [
#     'accounts.backends.EmailBackend',  # Custom email authentication
#     'django.contrib.auth.backends.ModelBackend',  # Fallback to default
# ]

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
RAZORPAY_KEY_ID = env('RAZORPAY_KEY_ID', default='rzp_live_RVQXMrxCQbvLxB')
RAZORPAY_KEY_SECRET = env('RAZORPAY_KEY_SECRET', default='aWlMkID7p0GccmP4ADyTLjYX')

# Email Configuration (Hardcoded for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pratapbag33@gmail.com'
EMAIL_HOST_PASSWORD = 'klnt subo hlqr yhry'  # Replace with actual Gmail app password
DEFAULT_FROM_EMAIL = 'biophysioconsultant@gmail.com'

# Login/Logout URLs
# LOGIN_URL = '/accounts/login/'
# LOGIN_REDIRECT_URL = '/dashboard/'
# LOGOUT_REDIRECT_URL = '/'

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

# Django Unfold Configuration
UNFOLD = {
    "SITE_TITLE": "Bio-Physio Consultant",
    "SITE_HEADER": "Bio-Physio Admin",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: get_site_logo_or_fallback(request),
    "SITE_LOGO": lambda request: get_site_logo_or_fallback(request),
    "SITE_SYMBOL": "favorite",  # Symbol from Material Design Icons
    "SHOW_HISTORY": True,  # Show history button
    "SHOW_VIEW_ON_SITE": True,  # Show view on site button
    "ENVIRONMENT": "healthcare_booking.utils.environment_callback",
    "DASHBOARD_CALLBACK": "healthcare_booking.utils.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),  # Login page background
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "STYLES": [
        lambda request: static("css/custom_admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/custom_admin.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in sidebar
        "show_all_applications": True,  # Show all applications in sidebar
        "navigation_expanded": True,  # Keep navigation expanded by default
        "navigation": [
            {
                "title": "Dashboard",
                "separator": False,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": lambda request: reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Bookings & Patients",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Bookings",
                        "icon": "calendar_month",
                        "link": lambda request: reverse_lazy("admin:bookings_booking_changelist"),
                    },
                    {
                        "title": "Services",
                        "icon": "medical_services",
                        "link": lambda request: reverse_lazy("admin:bookings_service_changelist"),
                    },
                    {
                        "title": "Users",
                        "icon": "group",
                        "link": lambda request: reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
            {
                "title": "Training & Career",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "New Batches",
                        "icon": "school",
                        "link": lambda request: reverse_lazy("admin:career_jobopening_changelist"),
                    },
                    {
                        "title": "Training Applications",
                        "icon": "description",
                        "link": lambda request: reverse_lazy("admin:career_jobapplication_changelist"),
                    },
                ],
            },
            {
                "title": "Contact Messages",
                "separator": True,
                "items": [
                    {
                        "title": "Contact Messages",
                        "icon": "mail",
                        "link": lambda request: reverse_lazy("admin:contact_contactmessage_changelist"),
                    },
                ],
            },
            {
                "title": "Content Management",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Blog Posts",
                        "icon": "article",
                        "link": lambda request: reverse_lazy("admin:blog_blogpost_changelist"),
                    },
                    {
                        "title": "Clinic Info",
                        "icon": "business",
                        "link": lambda request: reverse_lazy("admin:contact_clinicinfo_changelist"),
                    },
                ],
            },
            {
                "title": "Site Settings",
                "separator": True,
                "items": [
                    {
                        "title": "Site Settings",
                        "icon": "settings",
                        "link": lambda request: reverse_lazy("admin:site_settings_sitesettings_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "bookings.booking",
            ],
            "items": [
                {
                    "title": "All Bookings",
                    "link": lambda request: reverse_lazy("admin:bookings_booking_changelist"),
                },
                {
                    "title": "Pending",
                    "link": lambda request: reverse_lazy("admin:bookings_booking_changelist") + "?status__exact=pending",
                },
                {
                    "title": "Confirmed",
                    "link": lambda request: reverse_lazy("admin:bookings_booking_changelist") + "?status__exact=confirmed",
                },
            ],
        },
    ],
}
