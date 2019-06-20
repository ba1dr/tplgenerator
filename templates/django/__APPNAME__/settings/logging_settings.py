# -*- coding: utf-8 -*-


def get_logging_config(app_name, log_folder, apps=None, debug=False, use_console=False):
    apps = apps or []
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': log_folder + '/mainlog.log',
                'formatter': 'verbose',
            },
            'celeryfile': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': log_folder + '/tasks.log',
                'formatter': 'verbose',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', ],
                'level': 'INFO',
                'propagate': True,
            },
            'main': {
                'handlers': ['file', ],
                'level': 'DEBUG',
                'propagate': True,
            },
            'tasks': {
                'handlers': ['celeryfile', ],
                'level': 'DEBUG',
                'propagate': True,
            },
            'utils': {
                'handlers': ['file', ],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }
    # define loggers for every app
    for app in apps:
        if app not in LOGGING['loggers']:
            LOGGING['loggers'][app] = LOGGING['loggers']['main']

    if use_console:
        # make all loggers use the console.
        for logger in LOGGING['loggers']:
            if 'console' not in LOGGING['loggers'][logger]['handlers']:
                LOGGING['loggers'][logger]['handlers'] += ['console']

    return LOGGING
