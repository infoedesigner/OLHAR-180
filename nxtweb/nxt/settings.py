import os
from pathlib import Path

from decouple import config, Csv
from dj_database_url import parse as db_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)



ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://sistema.agencianxt.com.br']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # libs
    'bootstrap5',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'ckeditor',
    'django_celery_results',
    'django_celery_beat',
    # apps
    'nxt.core',
    'nxt.companies',
    'nxt.security',
    'nxt.media',
    'nxt.crawlers',
    'nxt.clients',
    'nxt.newsletter',
    'nxt.notifications',
    'nxt.mailer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'nxt.security.middleware.last_access_middleware',
    'nxt.security.middleware.expiration_access_middleware',
]

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

ROOT_URLCONF = 'nxt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # apps
                'nxt.security.context_processors.company_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'nxt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL', default='postgresql://nxt:nxt@127.0.0.1:5432/nxt', cast=db_url
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_THOUSAND_SEPARATOR = True

NUMBER_GROUPING = 3

THOUSAND_SEPARATOR = '.'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOOTSTRAP5 = {
    'set_placeholder': False,
    'success_css_class': '',
}

DATE_INPUT_FORMATS = ['%d/%m/%Y']

DATETIME_INPUT_FORMATS = ['%d/%m/%Y %H:%M', '%d/%m/%Y']

# ckeditor
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
    },
    'toolbar': 'NXT',
    'width': '100%',
    'toolbar_NXT': [
        {
            'name': 'clipboard',
            'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']
        },
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
        },
    ]
}

# auth
AUTH_USER_MODEL = 'security.User'
LOGIN_URL = 'security:login'
LOGIN_REDIRECT_URL = 'core:index'

# rest framework

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DATE_INPUT_FORMATS': ["%d/%m/%Y"],
    'DATE_FORMAT': '%d/%m/%Y',
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M',
}


NXT_CRAWLER_PATH = config('NXT_CRAWLER_PATH', default='')

EMAIL_DEBUG = False
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'sistema@agencianxt.com.br'

SITE_URL = 'http://sistema.agencianxt.com.br'

# Celery settings
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = config(
    'CELERY_BROKER_URL', "redis://localhost:6379"
)
CELERY_RESULT_BACKEND = config(
    'CELERY_RESULT_BACKEND', "redis://localhost:6379"
)
CELERY_TIMEZONE = TIME_ZONE
CELERYD_SOFT_TIME_LIMIT = 600

# if DEBUG:
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#     INSTALLED_APPS += ['debug_toolbar']
#     INTERNAL_IPS = ['127.0.0.1']
