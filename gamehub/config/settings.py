import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ['SECRET_KEY'] = 'django-insecure-5=qx+gt@jfv7wwiv(s1u#aztmo-t=r4o7@1y&wwfgw)$vf460z'
os.environ['Client_id'] = 'wm1nb6p094b62w3amq21mbbnx418hu'
os.environ['Client_secret'] = 'scur949jwewiphhxwqvuicuilbwmcc'
os.environ['Bearer_token'] = 'AAAAAAAAAAAAAAAAAAAAAKzZTQEAAAAAka8KZhKajSZfaXmr4ZOS0ncipl0' \
                             '%3DVkTwjUbKn4cIPUSgKz9UjxC632RpW2OIa0B7UKKjxaXNA7s9eG '

SECRET_KEY = os.environ.get('SECRET_KEY')
IGDB_CLIENT_ID = os.environ.get('Client_id')
IGDB_CLIENT_SECRET = os.environ.get('Client_secret')
TWITTER_BEARER_TOKEN = os.environ.get('Bearer_token')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gamehub',
    'users.apps.UsersConfig'
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'drkjuqni',
        'USER': 'drkjuqni',
        'PASSWORD': 'IYje3plhx5_nBTCKZm-ve1ZZqWxZtZvG',
        'HOST': 'hattie.db.elephantsql.com',
        'PORT': 5432
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

