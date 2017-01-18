import logging

from .base import *  # noqa

logging.disable(logging.WARNING)

DEBUG = True
ALLOWED_HOSTS = ['*']

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = False