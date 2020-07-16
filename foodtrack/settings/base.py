"""
Django settings for foodtrack project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from decouple import config
from dj_database_url import parse as db_url
import django.db.models.options as options
from datetime import datetime, timedelta
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
APP_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(APP_DIR))
# GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH')
INDEX_FILE="index.html"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #django-apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_better_admin_arrayfield.apps.DjangoBetterAdminArrayfieldConfig',
    #3nd party moduel
    
    'rest_framework',
    # 'rest_framework_simplejwt.token_blacklist'
    'django_fsm',
    'django_filters',
    'corsheaders',
    'django_extensions',
    'storages',

    'foodtrack',
    'authentication',
    'core',
    'mailing'
    
]


# FT_ENDPOINTS = [
#     'core',
# ]

# INSTALLED_APPS.extend(FT_ENDPOINTS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodtrack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, 'dist')],
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
]

AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
    ]

WSGI_APPLICATION = 'foodtrack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url
    )
}
print(DATABASES)


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'authentication.User'
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = False
USE_L10N = False
USE_TZ = True

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
# AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
# AWS_S3_SIGNATURE_VERSION = config('AWS_S3_SIGNATURE_VERSION')
# AWS_DEFAULT_ACL=None
# AWS_S3_FILE_OVERWRITE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

print(ROOT_DIR)
STATIC_URL = '/static/'
# Place static in the same location as webpack build files
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

 # add this block below MIDDLEWARE
CORS_ORIGIN_WHITELIST = (
    config('CORS_ORIGIN_WHITELIST', default="http://localhost:3000"),
)

# add the following just below STATIC_URL
MEDIA_URL = '/media/' # add this
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media') # add this


CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379')
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379')
# CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_RESULT_SERIALIZER = 'pickle'
# CELERY_ACCEPT_CONTENT = ['json', 'pickle']


FRONTEND_URL = config('FRONTEND_URL', "https://test.decoster.io")
# STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')
# print(ROOT_DIR)
# STATIC_URL=os.path.join(ROOT_DIR, "dist/")

# STATICFILES_DIRS = [
# ]

# GOOGLE_OAUTH2_KEY = config('GOOGLE_OAUTH2_KEY')
# GOOGLE_OAUTH2_SECRET = config('GOOGLE_OAUTH2_SECRET')
# FACEBOOK_KEY = config('FACEBOOK_KEY')
# FACEBOOK_SECRET = config('FACEBOOK_SECRET')


# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']


# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']

# SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.social_auth.associate_by_email',  # <- this line not included by default
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )

EMAIL_USE_TLS = config("EMAIL_USE_TLS",True)
EMAIL_HOST = config("EMAIL_HOST",'smtp.gmail.com')
EMAIL_HOST_USER = config("EMAIL_HOST_USER",'youremail@gmail.com')
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD",'yourpassword')
EMAIL_PORT = int(config("EMAIL_HOST_PORT", 587))


OPENCAGE_API_KEY = config('OPENCAGE_API_KEY')

CONTACT_EMAIL= config('CONTACT_EMAIL')
DOMAIN = config("DOMAIN")