from pathlib import Path

import dj_database_url

from bidr.manage import get_env_variable


# =========================================================================== #
#                             General Configuration                           #
# =========================================================================== #
MAIN_APP_NAME = 'bidr'

ROOT_URLCONF = MAIN_APP_NAME + '.urls'

SITE_ID = 1

DATE_FORMAT = 'l, F d, Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'l, F d, Y H:i'

LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
USE_TZ = True
TIMEZONE = "UTC"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    MAIN_APP_NAME + '.apps.auctions',
    MAIN_APP_NAME + '.apps.bids',
    MAIN_APP_NAME + '.apps.client',
    MAIN_APP_NAME + '.apps.core',
    MAIN_APP_NAME + '.apps.core.templatetags.CoreTemplatetagsConfig',
    MAIN_APP_NAME + '.apps.datatables',
    MAIN_APP_NAME + '.apps.datatables.templatetags.DatatablesTemplatetagsConfig',
    MAIN_APP_NAME + '.apps.items',
    MAIN_APP_NAME + '.apps.organizations',
    'raven.contrib.django.raven_compat',
    'django_ajax',
    'dj_database_url',
    'static_precompiler',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'widget_tweaks',
    'taggit',
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
]

# =========================================================================== #
#                    Authentication/Security Configuration                    #
# =========================================================================== #

LOGIN_URL = 'admin_login'
LOGIN_REDIRECT_URL = 'home'

SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTH_USER_MODEL = 'core.BidrUser'

SECRET_KEY = get_env_variable('BIDR_SECRET_KEY')

# =========================================================================== #
#                            Database Configuration                           #
# =========================================================================== #

DATABASES = {
    'default': dj_database_url.config(default=get_env_variable("DATABASE_URL"))
}


# =========================================================================== #
#                           Email/SMS Configuration                           #
# =========================================================================== #

# Outgoing email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bidrapp@gmail.com'
EMAIL_HOST_PASSWORD = get_env_variable('BIDR_EMAIL_PASSWORD')

# Set the server's email address (for sending emails only)
SERVER_EMAIL = 'Bidr Mail Relay Server <do-not-reply@bidrapp.com>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# =========================================================================== #
#                        Template, Asset Configuration                        #
# =========================================================================== #

PROJECT_DIR = Path(__file__).parents[2]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'debug': False,
        }
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

STATIC_ROOT = str(PROJECT_DIR.joinpath("static").resolve())
STATIC_URL = '/static/'

MEDIA_ROOT = str(PROJECT_DIR.joinpath("media").resolve())
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    str(PROJECT_DIR.joinpath(MAIN_APP_NAME, "static").resolve()),
)

STATIC_PRECOMPILER_OUTPUT_DIR = ""
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = False

# =========================================================================== #
#                              REST Configuration                             #
# =========================================================================== #

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGINATE_BY': 100
}

DJOSER = {
    'DOMAIN': 'bidrapp.com',
    'SITE_NAME': 'Bidrapp',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_AFTER_REGISTRATION': True,
    'LOGIN_AFTER_ACTIVATION': False,
    'SEND_ACTIVATION_EMAIL': False,
}

CORS_ORIGIN_ALLOW_ALL = True

# =========================================================================== #
#                            Logging Configuration                            #
# =========================================================================== #

RAVEN_CONFIG = {
    'dsn': get_env_variable('BIDR_SENTRY_DSN'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
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
        'django.server': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'django_ajax': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
    },
}
