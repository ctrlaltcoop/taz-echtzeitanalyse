import hashlib
import json
import os

from tazboard.core.settings import BASE_DIR


def get_mock_filepath_for_query(query):
    query_hash = hashlib.md5(json.dumps(query).encode()).hexdigest()
    return os.path.join(BASE_DIR, '..', 'api', 'tests', 'mocks', '{}.json'.format(query_hash))


def get_elastic_mock_response(body):
    with open(get_mock_filepath_for_query(body)) as mock_response:
        return json.loads(mock_response.read())
