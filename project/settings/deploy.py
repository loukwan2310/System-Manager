import os
from pathlib import Path

from decouple import config

DEBUG = False
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent.parent.parent.absolute()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', cast=str)
JWT_TOKEN_EXPIRE_HOURS = config('JWT_TOKEN_EXPIRE_HOURS', cast=int, default=8)
ALLOWED_HOSTS = ['*']
# SECURITY WARNING: don't run with debug turned on in production!


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    # 'fcm_django',
    # 'apps.authentication',
    'apps.users',
    # 'apps.exercises',
    # 'apps.missions',
    # 'apps.devices',
    # 'apps.notifications',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google'
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware"

]

ROOT_URLCONF = 'project.urls'

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
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', cast=str),
        'USER': config('DB_USER', cast=str),
        'PASSWORD': config('DB_PASS', cast=str),
        'HOST': 'localhost',
        'PORT': config('DB_PORT', cast=int),
        'TEST': {
            'NAME': config('DB_NAME', cast=str)
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
LANGUAGES = [
    ('en', 'English'),
    ('ja', 'Japanese'),
]
LANGUAGE_CODE = 'en'

TIME_ZONE = config('DEFAULT_TIME_ZONE', cast=str, default='UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'common.auth.JWTAuth'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user_login': '60/min',
    },
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'common.exceptions.api_error_handler',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPagination',
    'PAGE_SIZE': 10
}

DATA_UPLOAD_MAX_MEMORY_SIZE = config('DATA_UPLOAD_MAX_MEMORY_SIZE', cast=int, default=25 * 1024 * 1024)
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', cast=int, default=25 * 1024 * 1024)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Documentation',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CELERY_BROKER_URL = config('CELERY_BROKER_URL', cast=str)
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', cast=str)
CELERY_TASK_ANNOTATIONS = {'*': {'max_retries': 5, 'retry_backoff': 5}}
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_TRACK_STARTED = True

FITBIT_CLIENT_ID = config('FITBIT_CLIENT_ID', cast=str)
FITBIT_CLIENT_SECRET = config('FITBIT_CLIENT_SECRET', cast=str)
FITBIT_CODE_VERIFIER = config('FITBIT_CODE_VERIFIER', cast=str)
FITBIT_CODE_CHALLENGE = config('FITBIT_CODE_CHALLENGE', cast=str)
FITBIT_ACCESS_TOKEN_EXPIRE_HOURS = config('FITBIT_ACCESS_TOKEN_EXPIRE_HOURS', cast=int, default=24)

BASE_BACKEND_URL = "http://127.0.0.1:8000"
GOOGLE_OAUTH2_CLIENT_ID = "1018918224641-3uqu4jsf13ga7qs9mu9d020qheflljlo.apps.googleusercontent.com"
GOOGLE_OAUTH2_CLIENT_SECRET = "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"
GOOGLE_OAUTH2_PROJECT_ID = "django-oauth2-425714"
# REDIRECT_URI = "/api/v1/accounts/google-oauth2/login/callback"

# from allauth.socialaccount.providers.google import views

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': GOOGLE_OAUTH2_CLIENT_ID,
            'secret': GOOGLE_OAUTH2_CLIENT_SECRET,
            # 'key': GOOGLE_OAUTH2_PROJECT_ID
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'OAUTH_PKCE_ENABLED': True,
        'REDIRECT_URI': 'http://127.0.0.1:8000/api/v1/accounts/google-oauth2/login/callback'
    }
}
