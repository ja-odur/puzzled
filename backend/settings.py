"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from decouple import config
from backend.lib.settingstools import settings_vector

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(config('DEBUG'))

if DEBUG:
    ALLOWED_HOSTS = settings_vector.get_by_path('web.allowed_hosts.development', ['*', '127.0.0.1', 'localhost'])
else:
    ALLOWED_HOSTS = settings_vector.get_by_path('web.allowed_hosts.production')

BASE_URL = config('BASE_URL', 'http://localhost:8000/')

REDIS_URL = config('REDIS_URL', 'redis://localhost:6379/0')

REDIS_CACHE_PREFIX = None

DYNAMIC_CONFIGURATION_FILE = config('DYNAMIC_CONFIGURATION_FILE', None)

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'backend.authentication.apps.AuthenticationConfig',
    'backend.chat.apps.ChatConfig',
    'backend.email.apps.EmailConfig',
    'backend.fan_out.apps.FanOutConfig',
    'backend.gem.apps.GemConfig',
    'backend.poker.apps.PokerConfig',
    'backend.sudoku.apps.SudokuConfig',
    'frontend.apps.PuzzledFrontConfig',

    # third party apps
    'graphene_django',
    'webpack_loader',
    'django_q',
    'channels',
    'graphene_subscriptions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'NAME': 'jinja2',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,  # looks in each "jinja2" directory within apps
        'OPTIONS': {
            # callable invoked to create the Jinja2 environment
            'environment': 'backend.email.jinja2_env.environment',
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = "backend.routing.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URI'))
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Authentication
AUTH_USER_MODEL = 'authentication.User'
LOGIN_URL = '/u/sign-in/'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# This is where collectstatic will put all the static files it gathers.  These should then
# be served out from /static by the StaticFilesStorage
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

# This is where the files will be collected from when running `collectstatic`.
# From Django's perspective, this is the input location.
STATICFILES_DIRS = [
    'frontend/static',
]

STATIC_URL = '/static/'

if not DEBUG:
    raise ImproperlyConfigured('Please set the static-server')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

GRAPHENE = {
    'SCHEMA': 'backend.schema.schema',
    'SUBSCRIPTION_PATH': 'subscriptions/',
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'webpack_bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json')
    }
}

if not DEBUG:
    WEBPACK_LOADER['DEFAULT'].update({
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats-prod.json')
    })

# Django Email config
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

DEFAULT_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'backend.email.backends.django_q.DjangoQBackend'
DJANGO_Q_EMAIL_BACKEND = config('DJANGO_EMAIL_BACKEND', DEFAULT_BACKEND)
VERIFY_EMAIL_LINK_AGE = int(config('VERIFY_EMAIL_LINK_AGE', 8 * 60 * 60))  # 8-hours

# Django-q configs
Q_CLUSTER = {
    'name': 'puzzled',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'cpu_affinity': 1,
    'save_limit': 250,
    'queue_limit': 500,
    'label': 'Puzzled Q',
    'redis': config('REDIS_URL', 'redis://localhost:6379/0'),
}

# Gems
DEFAULT_GEMS = 0
