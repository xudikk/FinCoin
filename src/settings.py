#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = "Fintech Coin"

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 1)
DEBUG = bool(os.getenv('DEBUG') == 'True')
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS').split(',')

METHODS = os.getenv('AUTH_METHODS', '').split(',')

AUTH_USER_MODEL = 'core.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    # internal
    "core",

    # external
    'corsheaders',
    "bootstrap4",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'src.context_processors.user_type',
                'src.context_processors.notifications',
                'src.context_processors.basket',

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.' + os.getenv('DB_ENGINE', "mysql"),
            'NAME': os.getenv("POSTGRES_DB"),
            'USER': os.getenv("POSTGRES_USER"),
            'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv("POSTGRES_PORT"),
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
DEFAULT_LANG = "uz"

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Media files (docs, Images, files)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""  Extra settings """

# Cors

if not DEBUG:
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_URL').split(',')

    CSRF_TRUSTED_ORIGINS = os.getenv('CORS_URL').split(',')

    CORS_ORIGIN_WHITELIST = os.getenv('CORS_URL').split(',')

PAGINATE_BY = 15

LOGS_DIR = BASE_DIR / 'log'

EXTERNAL_TOKENS = {
    "sms": os.getenv('SMS_TOKEN')
}

EXTERNAL_URLS = {
    "sms": os.getenv('SMS_URL')
}

RANGE = int(os.getenv('RANGE', 5))
OTP_RANGE = 6

CUSTOM_HASHING = os.getenv("HASHING")
UNHASH = os.getenv("UNHASH")

HOST_URL = "http://127.0.0.1:8000"
