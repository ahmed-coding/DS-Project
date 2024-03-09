"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'apps.User'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-em_f#nu79yd6@j8vei##uicmg*gob*r#zj$34)@etsc#md6p6!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # internl apps
    'apps',
    # GIS and GeoDjango
    'django.contrib.gis',  # For Test GIS
    'rest_framework_gis',
    # external apps
    'corsheaders',
    'mptt',
    'rest_framework',
    'user_agents',
    # 'channels',
    # 'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'schema_graph',



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'  # ,
    # 'whitenoise.middleware.WhiteNoiseMiddleware',#
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'apps/templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = "core.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'USER': 'postgres',
    #     'NAME': 'DS',
    #     'HOST': 'postgres',
    #     'PORT': '5432',
    #     'PASSWORD': '12345',
    #     'TEST': {
    #             'NAME': 'mytestdatabase',
    #     },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'USER': 'postgres',
    #     'NAME': 'DS',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    #     'PASSWORD': '12345',
    #     'TEST': {
    #             'NAME': 'mytestdatabase',
    #     },
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static/",

]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = BASE_DIR / 'assets/'
MEDIA_URL = 'media/'
MEDIAFILES_DIRS = [
    BASE_DIR / "../media",
]
MEDIA_ROOT = BASE_DIR / '../media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Settings for Email
EMAIL_HOST = 'smtp.titan.email'
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'do-not-reply@ymall-ye.com'
EMAIL_HOST_PASSWORD = 'Yyyy7724!'
DEFUALT_FROM_EMAIL = EMAIL_HOST_USER
# End settings for Email


# Rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    'DEFAULT_PERMISSINS_CLASSES': ("rest_framework.permissions.IsAuthenticated",),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

CORS_ORIGIN_ALLOW_ALL = True  # -> Cors Header


CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:8000',
#     'http://192.168.1.100:8080',
# )


# Google
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')


# SPECTACULAR Swagger documentation settings
SPECTACULAR_SETTINGS = {
    'TITLE': ' API Documentation with Swagger UI for Ecommerce',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    # OTHER SETTINGS
}

# Channels settings
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("redis", 6379)],
#         },
#     },
# }


# # Celery settings with redis
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get(
#     "CELERY_BACKEND", "redis://redis:6379/0")

# Celery settings with rabbitmq
# CELERY_BROKER_URL = os.environ.get(
#     "CELERY_BROKER", "amqp://guest:guest@rabbitmq:5672/")
# CELERY_RESULT_BACKEND = os.environ.get(
#     "CELERY_BACKEND", "redis://redis:6379/0")
