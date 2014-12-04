import django
from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from whitenoise.django import DjangoWhiteNoise

django.setup()

# Send any wsgi errors to Sentry
application = Sentry(DjangoWhiteNoise(get_wsgi_application()))
