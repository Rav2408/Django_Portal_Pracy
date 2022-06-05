"""
Django settings for Django_Portal_Pracy project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5a^&z@d=951@cdcix4sgfjsq4r%cr1drprn8ihx823e_r@rxna'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6LczTeEfAAAAANM3rsBQ63TRXKhcJwHOT0skIhhY'
RECAPTCHA_PRIVATE_KEY = '6LczTeEfAAAAAEUfRIJXXfOxpT4DY0WWs4FTf1-R'

# Application definition

INSTALLED_APPS = [
    'Offers.apps.OffersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'livereload',
    'captcha',
    'crispy_forms',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'Django_Portal_Pracy.urls'

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
            'libraries': {
                'dict': 'templatetags.dict',
                }
        },
    },
]

WSGI_APPLICATION = 'Django_Portal_Pracy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fjqwduqu',
        'USER': 'fjqwduqu',
        'PASSWORD': '8HctFoeJknN5VodK6_BL8S4QO4eP9D5M',
        'HOST': 'rogue.db.elephantsql.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

#AUTH_PASSWORD_VALIDATORS = [
 #   {
 #       'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
 #   },
 #   {
 #       'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
 #   },
  #  {
  #      'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  #  },
  #  {
  #      'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  #  },
#]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
#     )

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
REGISTER_REDIRECT_URL = '/'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}