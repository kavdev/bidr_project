import django
from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
# from whitenoise.django import DjangoWhiteNoise
from dj_static import Cling, MediaCling

django.setup()

# Send any wsgi errors to Sentry
application = Sentry(Cling(MediaCling(get_wsgi_application())))
