"""
Base Settings
"""
import os
import sys
import socket
import logging.config
# from celery.schedules import crontab

# DEFINE PATHS
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CUR_DIR)
ROOT_DIR = os.path.dirname(APP_DIR)
APP_NAME = os.path.basename(APP_DIR)

sys.path.insert(0, os.path.join(APP_DIR, 'apps'))

DEBUG = True
SETTINGS_DIR = '/usr/local/etc'
LOG_FOLDER = f'/var/log/{APP_NAME}'
COMPANY_NAME = f"{APP_NAME}"

APPS = [
    'dashboards',
    'user_auth',
    'utils',
    'lib',
]

default_settings_file = os.path.join(CUR_DIR, 'settings.default.yaml')
settings_file = os.path.join(SETTINGS_DIR, f'{APP_NAME}.yaml')
USER_SETTINGS_FILE = settings_file

# See https://github.com/celery/billiard/issues/168
os.environ['JOBLIB_MULTIPROCESSING'] = '0'

CELERYBEAT_SCHEDULE = {
}

THIS_HOST_NAME = socket.getfqdn()
# http://stackoverflow.com/a/1267524/494631
# THIS_HOST_IP = [
#     l for l in
#     ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
#      if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
#                                           for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]
#      ) if l][0][0]

COGNITO_CLIENT_SECRET = None
CELERY_RESULT_BACKEND = 'redis://?new_join=1'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
REDIS_URL = 'redis://localhost:6379/9'
SEMAPHORES_REDIS_URL = 'redis://localhost:6379/9'
# BROKER_URL = "amqp://modis:modis@localhost:5672/modis/"
BROKER_URL = REDIS_URL
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
BROKER_HEARTBEAT = 30
CELERY_ACKS_LATE = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_RESULT_EXPIRES = 24 * 60 * 60 * 7  # after 7 days results of tasks will expire
CELERYD_PREFETCH_MULTIPLIER = 1  # Recommended with Redis
CELERY_DEFAULT_DELIVERY_MODE = 'transient'  # To improve the performane of the broker
CELERY_TRACK_STARTED = True
