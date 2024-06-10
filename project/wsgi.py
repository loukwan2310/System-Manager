"""
WSGI config for main project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from decouple import config
from django.core.wsgi import get_wsgi_application

PRODUCTION = config('PRODUCTION', cast=bool, default=False)
if PRODUCTION:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.deploy')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.dev')

application = get_wsgi_application()
