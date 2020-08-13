import dj_database_url

from .base import *  # noqa: F403, F401
from .base import *  # noqa: F403, F401

DATABASES = {
    'default': dj_database_url.config()
}
