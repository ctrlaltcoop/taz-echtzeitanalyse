from .base import *  # noqa: F403, F401

SECRET_KEY = 'dummysecret'

# need dummy DB in tests as LiveServerTestCase depends on it
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
  }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'FATAL',
    },
}
