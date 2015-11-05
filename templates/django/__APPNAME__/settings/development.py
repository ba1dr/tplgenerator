"""
Development Settings
"""
from .base import *

DEBUG = True
# TEMPLATE_DEBUG = True

APPS = (
    'django_extensions',
)

INSTALLED_APPS += APPS

INTERNAL_IPS = ('127.0.0.1',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'compressor.finders.CompressorFinder',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BROKER_URL = 'sqla+sqlite:///celery_brokerdb.sqlite'
CELERY_RESULT_BACKEND = 'db+sqlite:///celery_resultsdb.sqlite'
