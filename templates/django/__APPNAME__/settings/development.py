"""
Development Settings
"""
from .base import *


SECRET_KEY = 'V2jyi4^e*ezt0)ds1KyNV#^pj6kXVGbHMGL$u%!oiE7zNOcBEu@'

DEBUG = True
# TEMPLATE_DEBUG = True

LOCAL_APPS = [
    # 'debug_toolbar',
    # 'django_extensions',
]

INTERNAL_IPS = ('127.0.0.1',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'compressor.finders.CompressorFinder',
)

DEBUG_TOOLBAR_PANELS = [
    # 'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    # 'SHOW_TOOLBAR_CALLBACK': 'ddt_request_history.panels.request_history.allow_ajax',
    'SHOW_TEMPLATE_CONTEXT': True,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BROKER_URL = 'sqla+sqlite:///%s' % os.path.join(ROOT_DIR, 'celery_brokerdb.sqlite')
CELERY_RESULT_BACKEND = 'db+sqlite:///%s' % os.path.join(ROOT_DIR, 'celery_resultsdb.sqlite')
