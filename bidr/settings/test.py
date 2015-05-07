"""
Test Settings

http://www.daveoncode.com/2013/09/23/effective-tdd-tricks-to-speed-up-django-tests-up-to-10x-faster/
"""


import logging

from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_ajax',
    'static_precompiler',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'taggit',
    'bidr.apps.auctions',
    'bidr.apps.core',
    'bidr.apps.core.templatetags.CoreTemplatetagsConfig',
    'bidr.apps.datatables',
    'bidr.apps.datatables.templatetags.DatatablesTemplatetagsConfig',
    'bidr.apps.bids',
    'bidr.apps.items',
    'bidr.apps.organizations',
)

DEBUG = False
TEMPLATE_DEBUG = False
logging.disable(logging.CRITICAL)
