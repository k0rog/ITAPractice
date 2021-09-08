import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# У меня винда, поэтому баш циклы, которые в интернетике предлагают - не подходят
# И команды export, соответственно, нет. Её windows-аналог SET почему-то не работает.
# Поэтому (пока что) я захардкодил токены. Пользуйся, если нужно :)
# Чуть позже обязательно поищу решение
os.environ['SECRET_KEY'] = 'django-insecure-5=qx+gt@jfv7wwiv(s1u#aztmo-t=r4o7@1y&wwfgw)$vf460z'
os.environ['Client_id'] = 'wm1nb6p094b62w3amq21mbbnx418hu'
os.environ['Client_secret'] = 'scur949jwewiphhxwqvuicuilbwmcc'
os.environ['Bearer_token'] = 'AAAAAAAAAAAAAAAAAAAAAKzZTQEAAAAAka8KZhKajSZfaXmr4ZOS0ncipl0' \
                             '%3DVkTwjUbKn4cIPUSgKz9UjxC632RpW2OIa0B7UKKjxaXNA7s9eG '

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
            'libraries': {
                'filters': 'gamehub.filters',
            }
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'UTC+3'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
