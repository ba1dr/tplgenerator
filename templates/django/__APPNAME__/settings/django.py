
from .base import *

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CUR_DIR)
APP_NAME = os.path.basename(APP_DIR)

ADMINS = (
    # ('admin', 'admin@localhost'),
)

# CORE SETTINGS
DEBUG = False
ALLOWED_HOSTS = []
ROOT_URLCONF = f'{APP_NAME}.urls'
WSGI_APPLICATION = f'{APP_NAME}.wsgi.application'
AUTH_USER_MODEL = 'user_auth.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# APP DECLARATIONS
DJANGO_APPS = [
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    # 'suit',
    'jet.dashboard',
    'jet',
    # 'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'channels'
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'registration',
    'imagekit',
    'django_extensions',
]

LOCAL_APPS = [
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    os.path.join(ROOT_DIR, 'locale'),
]
LOCALE_PATHS += [os.path.join(ROOT_DIR, a, 'locale') for a in LOCAL_APPS]
LANGUAGES = (
    ('en', 'English'),
)

# STATIC AND MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(APP_DIR, 'public'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

# This would be good to use for file storage, especially user uploads
# DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'

# TEMPLATES
TEMPLATES = [
    {
        # 'TEMPLATE_DEBUG': DEBUG,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                # 'django.core.context_processors.static',
                'utils.context_processors.common_context',
                'django.template.context_processors.tz',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'
ACCOUNT_ACTIVATION_DAYS = 7
