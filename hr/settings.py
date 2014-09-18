# -*- coding:utf-8 -*-
"""
Django settings for hr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0!ja^kt$=n5xr%07kk4p!h#5z%ft#w9p61r=sf0va4!#(n2uxc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'labour',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'hr.urls'

WSGI_APPLICATION = 'hr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Chongqing'

#admin页面时间格式
DATETIME_FORMAT = 'Y-m-d H:i:s'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, os.path.join(os.pardir, "media"))

MEDIA_URL = "/media/"

#logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/labour_info.log',
            'formatter': 'verbose',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/labour_info.log',
            'formatter': 'verbose',
        },
        'login': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/login_info.log',
            'formatter': 'verbose',
        },
        'err': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/labour_error.log',
            'formatter': 'verbose',
        },
        
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'debug': {
            'handlers': ['debug'],
            'level': 'DEBUG',
        },
        'info': {
            'handlers': ['info'],
            'level': 'INFO',
        },
        'login': {
            'handlers': ['login'],
            'level': 'INFO',
        },
        'err': {
            'handlers': ['err'],
            'level': 'ERROR',
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass

