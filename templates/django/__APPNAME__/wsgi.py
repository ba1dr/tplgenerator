"""
WSGI config for this project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

dirname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(dirname))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{os.path.basename(dirname)}.settings")

application = get_wsgi_application()
