import hashlib
import json
import os

from tazboard.api.queries.constants import MOCK_FAKE_NOW
from tazboard.api.utils.datetime import round_to_seconds
from tazboard.core.settings import BASE_DIR


def get_mock_filepath_for_query(query):
    query_hash = hashlib.md5(json.dumps(query).encode()).hexdigest()
    return os.path.join(BASE_DIR, '..', 'api', 'tests', 'mocks', '{}.json'.format(query_hash))


def get_mock_test_sample_path_for_query_function(query_function):
    return os.path.join(BASE_DIR, '..', 'api', 'tests', 'mocks', '{}-sample.json'.format(query_function.__name__))


def get_elastic_mock_response(body):
    with open(get_mock_filepath_for_query(body)) as mock_response:
        return json.loads(mock_response.read())


def rewrite_query_params(original_function):
    def wrapper(min_date, max_date, *args, **kwargs):
        delta = max_date - min_date
        fake_max = MOCK_FAKE_NOW
        fake_min = round_to_seconds(fake_max - delta)
        return original_function(fake_min, fake_max, *args, **kwargs)
    return wrapper


def activate_global_elastic_mocks():
    from tazboard.api import views
    from ..elastic_client import es

    views.get_histogram_query = rewrite_query_params(views.get_histogram_query)
    views.get_toplist_query = rewrite_query_params(views.get_toplist_query)
    views.get_referrer_query = rewrite_query_params(views.get_referrer_query)
    views.get_devices_query = rewrite_query_params(views.get_devices_query)
    views.get_total_query = rewrite_query_params(views.get_total_query)

    es.search = get_elastic_mock_response
