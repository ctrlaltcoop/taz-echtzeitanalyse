import json
from datetime import timedelta

from django.core.management import BaseCommand

from tazboard.api.elastic_client import es
from tazboard.api.queries.constants import MOCK_FAKE_NOW
from tazboard.api.queries.histogram import get_histogram_query
from tazboard.api.queries.referrer import get_referrer_query
from tazboard.api.queries.toplist import get_toplist_query
from tazboard.api.tests.common import get_mock_filepath_for_query, get_mock_test_sample_path_for_query_function
from tazboard.api.utils.datetime import round_to_seconds


def get_argument_matrix(list_a, list_b):
    for i in list_a:
        for j in list_b:
            yield i + j


class Command(BaseCommand):
    query_configs = [
        {
            'get_query': get_histogram_query,
            'arguments': [
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=24)), MOCK_FAKE_NOW),
            ]
        },
        {
            'get_query': get_referrer_query,
            'arguments': [
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(minutes=15)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(minutes=30)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=1)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=6)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=24)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=7)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=30)), MOCK_FAKE_NOW),
            ]
        },
        {
            'get_query': get_toplist_query,
            'arguments': get_argument_matrix((
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(minutes=15)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(minutes=30)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=1)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=6)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=24)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=7)), MOCK_FAKE_NOW),
                (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=30)), MOCK_FAKE_NOW),
            ), ((10,), (25,)))
        }
    ]

    def handle(self, *args, **options):
        for config in self.query_configs:
            for index, arguments in enumerate(config['arguments']):

                query_fn = config['get_query']
                query = query_fn(*arguments)
                response = es.search(body=query)
                with open(get_mock_filepath_for_query(query), 'w') as outfile:
                    outfile.write(json.dumps(response, indent=4))
                # put aside one sample for e2e tests
                if index == 0:
                    with open(get_mock_test_sample_path_for_query_function(query_fn), 'w') as outfile:
                        outfile.write(json.dumps(response, indent=4))
