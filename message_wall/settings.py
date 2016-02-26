"""
Django settings for message_wall project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b+2^0f1n#7%-(tuom60uwy3n&6a6rmprfx4-d%!k!5wz__2!)+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'wall_app',
    'mptt',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'message_wall.urls'

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
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'message_wall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'wall_app.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Python social auth settings

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'

LOGIN_ERROR_URL = '/'


# OAuth social networks settings

SOCIAL_AUTH_VK_OAUTH2_KEY = '5100070'

SOCIAL_AUTH_VK_OAUTH2_SECRET = 'EXQixGVB8Pk5Q7AFyufI'

SOCIAL_AUTH_FACEBOOK_KEY = '646704275472612'

SOCIAL_AUTH_FACEBOOK_SECRET = '883b6d06061578fef586a860b3fee95b'

# SOCIAL_AUTH_TWITTER_KEY = 'DjiOdI8nDxYvBJUzMGulohETD'
# SOCIAL_AUTH_TWITTER_SECRET = 'WiAZ2pbO0ttMdyCLZU32shceQkN2hQGUSARhr8DGBuRjQHl4Va'

# SOCIAL_AUTH_INSTAGRAM_KEY = '0287e3d98d454bd9b01ee57b5bc46830'
# SOCIAL_AUTH_INSTAGRAM_SECRET = '1502efae83e44105bfad8a2ba1d9b976'

# SOCIAL_AUTH_GOOGLE_PLUS_KEY = '459351663494-jcleer2u1ni9j1b0giigsh68e9nk6ump.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'oH8AUFUC1kpCrQTXpJk5SIO9'
# SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = ['https://www.googleapis.com/auth/plus.login']