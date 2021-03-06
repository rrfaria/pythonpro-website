"""
Django settings for pythonpro project.

Generated by 'django-admin startproject' using Django 2.0b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
from functools import partial

import sentry_sdk
from decouple import Csv, config
from dj_database_url import parse as dburl
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

# Control subscriptions ads and payment.
SUBSCRIPTIONS_OPEN = config('SUBSCRIPTIONS_OPEN', cast=bool)

METEORIC_LAUNCH_OPEN = config('METEORIC_LAUNCH_OPEN', cast=bool)

PAGARME_CRYPTO_KEY = config('PAGARME_CRYPTO_KEY')
PAGARME_API_KEY = config('PAGARME_API_KEY')

CHAVE_PAGARME_API_PRIVADA = PAGARME_API_KEY
CHAVE_PAGARME_CRIPTOGRAFIA_PUBLICA = PAGARME_CRYPTO_KEY


PAGSEGURO_PAYMENT_PLAN = config('PAGSEGURO_PAYMENT_PLAN')

# Email Configuration

DEFAULT_FROM_EMAIL = 'suporte@python.pro.br'

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Login Config

LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# Application definition

INSTALLED_APPS = [
    'pythonpro.core',
    'pythonpro.discourse',
    'pythonpro.modules',
    'pythonpro.payments',
    'pythonpro.cohorts',
    'pythonpro.email_marketing',
    'pythonpro.dashboard',
    'pythonpro.launch',
    'pythonpro.analytics',
    'pythonpro.checkout',
    'pythonpro.redirector',
    'pythonpro.pages',
    'rolepermissions',
    'ordered_model',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.staticfiles',
    'django_extensions',
    'bootstrap4',
    'django_pagarme',
    'phonenumber_field',
]

MIDDLEWARE = [
    'pythonpro.core.middleware.SSLMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pythonpro.analytics.middleware.AnalyticsMiddleware',
]

ROLEPERMISSIONS_MODULE = 'pythonpro.core.roles'

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

# Discourse config
DISCOURSE_BASE_URL = config('DISCOURSE_BASE_URL', default='')
DISCOURSE_SSO_SECRET = config('DISCOURSE_SSO_SECRET')
DISCOURSE_API_USER = config('DISCOURSE_API_USER')
DISCOURSE_API_KEY = config('DISCOURSE_API_KEY')

ROOT_URLCONF = 'pythonpro.urls'

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
                'pythonpro.core.context_processors.global_settings',
                'pythonpro.modules.context_processors.global_settings',
                'pythonpro.cohorts.context_processors.global_settings',
                'pythonpro.payments.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'pythonpro.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

if 'localhost' not in ALLOWED_HOSTS:
    dburl = partial(dburl, conn_max_age=600, ssl_require=True)

DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=dburl),
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'core.User'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

# for phone validation
PHONENUMBER_DEFAULT_REGION = 'BR'

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Configuration for dev environment
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COLLECTFAST_ENABLED = False

# STORAGE CONFIGURATION IN S3 AWS
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = config('DJANGO_AWS_ACCESS_KEY_ID', default=False)
if AWS_ACCESS_KEY_ID:  # pragma: no cover
    COLLECTFAST_ENABLED = True
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
    INSTALLED_APPS.append('s3_folder_storage')
    INSTALLED_APPS.append('storages')
    AWS_SECRET_ACCESS_KEY = config('DJANGO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('DJANGO_AWS_STORAGE_BUCKET_NAME')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_PRELOAD_METADATA = True
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_CUSTOM_DOMAIN = None

    AWS_DEFAULT_ACL = 'public-read'

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7

    # Revert the following and use str after the above-mentioned bug is fixed in
    # either django-storage-redux or boto
    control = f'max-age={AWS_EXPIRY:d}, s-maxage={AWS_EXPIRY:d}, must-revalidate'

    # Upload Media Folder
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = f'/{DEFAULT_S3_PATH}/'
    MEDIA_URL = f'//{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{DEFAULT_S3_PATH}/'

    # Static Assets
    # ------------------------------------------------------------------------------
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = 'static'
    STATIC_ROOT = f'/{STATIC_S3_PATH}/'
    STATIC_URL = f'//{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{STATIC_S3_PATH}/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# ------------------------------------------------------------------------------

# Configuring Sentry
SENTRY_DSN = config('SENTRY_DSN', default=None)

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()]
    )

# Active Campaign Configuration
ACTIVE_CAMPAIGN_URL = config('ACTIVE_CAMPAIGN_URL')
ACTIVE_CAMPAIGN_KEY = config('ACTIVE_CAMPAIGN_KEY')
ACTIVE_CAMPAIGN_TURNED_ON = config('ACTIVE_CAMPAIGN_TURNED_ON', cast=bool, default=True)

# Google Tag Manager Configuration
GOOGLE_TAG_MANAGER_ID = config('GOOGLE_TAG_MANAGER_ID')

# Celery config


BROKER_URL = config('CLOUDAMQP_URL')

CELERY_RESULT_BACKEND = config('REDIS_URL')
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
