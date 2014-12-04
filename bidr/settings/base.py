import os

from django.core.exceptions import ImproperlyConfigured

import dj_database_url
from unipath import Path


def get_env_variable(name):
    """ Gets the specified environment variable.

    :param name: The name of the variable.
    :type name: str
    :returns: The value of the specified variable.
    :raises: **ImproperlyConfigured** when the specified variable does not exist.

    """

    try:
        return os.environ[name]
    except KeyError:
        error_msg = "The %s environment variable is not set!" % name
        raise ImproperlyConfigured(error_msg)


# ======================================================================================================== #
#                                         General Management                                               #
# ======================================================================================================== #

ADMINS = (
    ('Alex Kavanaugh', 'kavanaugh.development@outlook.com'),
)

MANAGERS = ADMINS

# ======================================================================================================== #
#                                         General Settings                                                 #
# ======================================================================================================== #

# Local time zone for this installation. Choices can be found here:
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

DATE_FORMAT = 'l, F d, Y'

TIME_FORMAT = 'h:i a'

DATETIME_FORMAT = 'l, F d, Y h:i a'

DEFAULT_CHARSET = 'utf-8'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

ROOT_URLCONF = 'bidr.urls'

# ======================================================================================================== #
#                                          Database Configuration                                          #
# ======================================================================================================== #

DATABASES = {
    'default': dj_database_url.config(default=get_env_variable('BIDR_DATABASE_URL')),
}

# ======================================================================================================== #
#                                            E-Mail Configuration                                          #
# ======================================================================================================== #

# Outgoing email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # This configuration uses the SMTP protocol as a backend
# EMAIL_HOST = 'mail.calpoly.edu'  # The host to use for sending email. Set to empty string for localhost.
# EMAIL_PORT = 25  # The port to use. Defaul values: 25, 587
# EMAIL_USE_TLS = True  # Whether or not to use SSL (Boolean)
# EMAIL_HOST_USER = get_env_variable('BIDR_EMAIL_USERNAME')
# EMAIL_HOST_PASSWORD = get_env_variable('BIDR_EMAIL_PASSWORD')

# Set the server's email address (for sending emails only)
SERVER_EMAIL = 'Bidr Mail Relay Server <do-not-reply@bidr.herokuapp.com>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# ======================================================================================================== #
#                                              Access Permissions                                          #
# ======================================================================================================== #

auction_manager_access_test = (lambda user: True)
auction_administrator_access_test = (lambda user: True)

# ======================================================================================================== #
#                                        Authentication Configuration                                      #
# ======================================================================================================== #

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/login/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'core.Bidder'

# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie settings.
SESSION_COOKIE_HTTPONLY = True

# Session expiraton
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('BIDR_SECRET_KEY')

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

PROJECT_DIR = Path(__file__).ancestor(3)

# The directory that will hold user-uploaded files.
MEDIA_ROOT = PROJECT_DIR.child("media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
MEDIA_URL = '/media/'

# The directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = PROJECT_DIR.child("static")

# URL prefix for static files. Make sure to use a trailing slash.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_DIR.child("bidr", "static"),
)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    PROJECT_DIR.child("bidr", "templates"),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'django_ajax',
    'dj_database_url',
    'rest_framework',
    'bidr.apps',
    'bidr.apps.core',
    'bidr.apps.bids',
)

# ======================================================================================================== #
#                                       REST Endpoint Configuration                                        #
# ======================================================================================================== #

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGINATE_BY': 10
}

# ======================================================================================================== #
#                                         Logging Configuration                                            #
# ======================================================================================================== #

RAVEN_CONFIG = {
    'dsn': get_env_variable('BIDR_SENTRY_DSN'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django_auth_ldap': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
        'django_ajax': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
    }
}

