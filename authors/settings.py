"""
Django settings for authors project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import environ
import datetime
import os

"""
Create a .env file in you root folder(ah-jarvis/)
The .env file holds all the details of the database, secret key and debug mode
Copy the details as they are in the env.example file in the root folder
Paste them on your .env and the run the app
"""

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(root('.env'))
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
JWT_SECRET_KEY = env('JWT_SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_extensions',
    'rest_framework',
    'social_django',
    'notifications',

    'authors.apps.authentication',
    'authors.apps.core',
    'authors.apps.profiles',
    'authors.apps.articles',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'authors.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "authors/apps/core/templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'authors.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

'''
Check the env.example file to get the idea of how your .env will be structured
Check the setup.md file for instructions to set up postgres database url
'''


DATABASES = {
    'default': env.db()
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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = (
    '0.0.0.0:4000',
    'localhost:4000',
)

# Tell Django about the custom `User` model we created. The string
# `authentication.User` tells Django we are referring to the `User` model in
# the `authentication` module. This module is registered above in a setting
# called `INSTALLED_APPS`.
AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'authors.apps.core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authors.apps.authentication.backends.JWTAuthentication',
    ),
}

VERIFCATION_URL = "http://localhost:6000/verify/"

AUTHENTICATION_BACKENDS = (
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('GOOGLE_SECRET')
# Scope
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = ['email', 'username']

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = env('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email',
}
FACEBOOK_EXTENDED_PERMISSIONS = ['email']


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
# Email configurations
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# JWT_EXPIRATION_DELTA set to default 1 day
JWT_EXPIRATION_DELTA = datetime.timedelta(
    seconds=env("JWT_EXPIRATION_SECONDS", default=86400))

CELERY_BROKER_URL = 'amqp://localhost'
