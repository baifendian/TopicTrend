"""
WSGI config for waka_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = open(os.path.join(BASE_DIR, 'ENV')).readline().strip()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waka_web.settings.%s"%env_file)

application = get_wsgi_application()
