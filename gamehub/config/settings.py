import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ['SECRET_KEY'] = 'django-insecure-5=qx+gt@jfv7wwiv(s1u#aztmo-t=r4o7@1y&wwfgw)$vf460z'
os.environ['Client_id'] = 'wm1nb6p094b62w3amq21mbbnx418hu'
os.environ['Client_secret'] = 'scur949jwewiphhxwqvuicuilbwmcc'
os.environ['Bearer_token'] = 'AAAAAAAAAAAAAAAAAAAAAKzZTQEAAAAAka8KZhKajSZfaXmr4ZOS0ncipl0' \
                             '%3DVkTwjUbKn4cIPUSgKz9UjxC632RpW2OIa0B7UKKjxaXNA7s9eG '
os.environ['DB_name'] = 'vcuatnce'
os.environ['DB_password'] = 'v0eYeBwxnm2N4_tVc7SJgA787h-Rt447'
os.environ['Email_sender'] = 'avramneoko6@gmail.com'
os.environ['Email_password'] = '321ilyxazc'


IGDB_CLIENT_ID = os.environ.get('Client_id')
IGDB_CLIENT_SECRET = os.environ.get('Client_secret')
TWITTER_BEARER_TOKEN = os.environ.get('Bearer_token')

DB_NAME = os.environ.get('DB_name')
DB_PASSWORD = os.environ.get('DB_password')

DEFAULT_FROM_EMAIL = os.environ.get('Email_sender')
EMAIL_HOST_USER = os.environ.get('Email_sender')
EMAIL_HOST_PASSWORD = os.environ.get('Email_password')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SECRET_KEY = os.environ.get('SECRET_KEY')

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
        'NAME': DB_NAME,
        'USER': DB_NAME,
        'PASSWORD': DB_PASSWORD,
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

LOGOUT_REDIRECT_URL = 'games'

