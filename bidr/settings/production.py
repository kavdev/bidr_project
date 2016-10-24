from .base import *  # noqa: F403

SESSION_COOKIE_NAME = 'BIDRSessionID'

ALLOWED_HOSTS = [
    'bidrapp.com',
    'bidr.herokuapp.com',
]

DEBUG = False  # noqa: F405
TEMPLATES[0]['OPTIONS']['debug'] = False  # noqa: F405

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = get_env_variable('BIDR_AWS_ACCESS_KEY_ID')  # noqa: F405
AWS_SECRET_ACCESS_KEY = get_env_variable('BIDR_AWS_SECRET_ACCESS_KEY')  # noqa: F405
AWS_STORAGE_BUCKET_NAME = 'bidr-images'
AWS_AUTO_CREATE_BUCKET = True

AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True

STATIC_URL = '//messagemanager.s3.amazonaws.com/static/'
MEDIA_URL = '//messagemanager.s3.amazonaws.com/media/'
