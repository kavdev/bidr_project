from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie Settings
SESSION_COOKIE_NAME = 'BIDRSessionID'

ALLOWED_HOSTS = [
    'bidrapp.com',
    'bidr.herokuapp.com',
    'bidr-staging.herokuapp.com'
]
