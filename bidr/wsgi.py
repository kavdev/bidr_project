import django
from django.core.handlers.wsgi import WSGIHandler
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

django.setup()

# Send any wsgi errors to Sentry
application = Sentry(WSGIHandler())
