"""
Django settings for DidactAI project.

A comprehensive educational content management and AI generation platform.
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,testserver,didactai.onrender.com', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'rest_framework',
    'corsheaders', 
    'crispy_forms',
    'crispy_tailwind',
    'rosetta',  # For translations
    
    # Local apps
    'accounts',
    'courses',
    'uploads', 
    'ai_generator',
    'exports',
    'analytics',
    'core',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For i18n
    # 'core.i18n.LanguageMiddleware',  # Custom language detection - keep disabled to stay in English
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'didactia_project.urls'

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
                'django.template.context_processors.i18n',  # Re-enabled for i18n
                # 'core.i18n.translation_context',  # Keep disabled - custom translation
            ],
        },
    },
]

WSGI_APPLICATION = 'didactia_project.wsgi.application'

# Database Configuration
DATA_DIR = Path(config('RENDER_DISK_PATH', default=BASE_DIR))
DATABASE_URL = config('DATABASE_URL', default=f'sqlite:///{DATA_DIR / "db.sqlite3"}')

try:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    # Test if this is a PostgreSQL URL but psycopg2 is not available
    if 'postgresql' in DATABASE_URL.lower():
        try:
            import psycopg2
        except ImportError:
            print("WARNING: PostgreSQL URL provided but psycopg2 not available. Falling back to SQLite.")
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': DATA_DIR / 'db.sqlite3',
                }
            }
except Exception as e:
    print(f"Database configuration error: {e}. Using SQLite fallback.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATA_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',  # Custom backend for email/username login
    'django.contrib.auth.backends.ModelBackend',     # Default Django backend
]

# Password validation
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

# Internationalization and Encoding
LANGUAGE_CODE = 'en'  # Default to English interface
TIME_ZONE = 'UTC'
USE_I18N = True  # Enable internationalization
USE_TZ = True

# Character encoding settings
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Language settings  
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('es', 'Spanish'), 
    ('de', 'German'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ru', 'Russian'),
    ('ar', 'Arabic'),
    ('zh', 'Chinese'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('hi', 'Hindi'),
    ('tr', 'Turkish'),
    ('el', 'Greek'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = DATA_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = config('MAX_UPLOAD_SIZE', default=50000000, cast=int)  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = config('MAX_UPLOAD_SIZE', default=50000000, cast=int)

# AI Configuration
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
HUGGINGFACE_API_TOKEN = config('HUGGINGFACE_API_TOKEN', default='')

# Storage Configuration
SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_KEY = config('SUPABASE_KEY', default='')
SUPABASE_SERVICE_KEY = config('SUPABASE_SERVICE_KEY', default='')

# AWS S3 Configuration (if using S3)
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')

# Celery Configuration (for background tasks)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='DidactAI <noreply@DidactAI.com>')
SERVER_EMAIL = config('SERVER_EMAIL', default='DidactAI <noreply@DidactAI.com>')
SERVER_NAME = config('SERVER_NAME', default='localhost:8000')

# Security Settings for Production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'DidactAI.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Application-specific settings
DidactAI_SETTINGS = {
    'ALLOWED_FILE_EXTENSIONS': config('ALLOWED_FILE_EXTENSIONS', default='pdf,docx,pptx,png,jpg,jpeg', cast=lambda v: [s.strip() for s in v.split(',')]),
    'MAX_FILE_SIZE': config('MAX_UPLOAD_SIZE', default=50000000, cast=int),
    'SUPPORTED_LANGUAGES': config('SUPPORTED_LANGUAGES', default='en,fr,es,de,it,pt,ru,ar,zh,ja,ko,hi,tr,el', cast=lambda v: [s.strip() for s in v.split(',')]),
    'DEFAULT_AI_MODEL': 'gemini-2.5-flash',
    'EXAM_VERSIONS_COUNT': 3,  # A, B, C versions
    'AUTO_DELETE_DAYS': 90,  # Auto-delete old files after 90 days
    'ENABLE_VERSIONING': True,  # Enable content versioning
    'MAX_VERSIONS_PER_OBJECT': 50,  # Maximum versions to keep
    'ANALYTICS_RETENTION_DAYS': 365,  # Analytics data retention
    'ENABLE_AI_TRANSLATION': True,  # Enable AI-powered translation
    'DEFAULT_TRANSLATION_SERVICE': 'google_translate',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production configurations
if not DEBUG:
    # Security settings for production
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Static file serving in production - Use simple storage temporarily
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    
    # CORS settings for production
    CORS_ALLOWED_ORIGINS = [
        'https://didactai.onrender.com',
    ]
    CORS_ALLOW_CREDENTIALS = True

# Crispy Forms Configuration  
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

