import json
from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand

from tazboard.api.elastic_client import es
from tazboard.api.queries.constants import MOCK_FAKE_NOW, MOCK_CXML_PATH
from tazboard.api.queries.devices import get_devices_query
from tazboard.api.queries.histogram import get_histogram_query
from tazboard.api.queries.referrer import get_referrer_query
from tazboard.api.queries.subjects import get_subjects_query
from tazboard.api.queries.toplist import get_toplist_query
from tazboard.api.queries.total import get_total_query
from tazboard.api.queries.fireplace import get_fireplace_query, fetch_ressort_cxml
from tazboard.api.tests.common import get_mock_filepath_for_query, get_mock_test_sample_path_for_query_function
from tazboard.api.utils.tazdatetime import round_to_seconds
from tazboard.api.utils.msearch_queries import prepare_msearch_query


def get_argument_matrix(list_a, list_b):
    for i in list_a:
        for j in list_b:
            yield i + j


FAKE_TIMEFRAMES = (
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(minutes=15)), MOCK_FAKE_NOW),
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(minutes=30)), MOCK_FAKE_NOW),
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=1)), MOCK_FAKE_NOW),
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=6)), MOCK_FAKE_NOW),
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(hours=24)), MOCK_FAKE_NOW),
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=7)), MOCK_FAKE_NOW)
    # (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=30)), MOCK_FAKE_NOW)
)


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
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_toplist_query,
            'arguments': get_argument_matrix(FAKE_TIMEFRAMES, ((10,), (100,)))
        },
        {
            'get_query': get_devices_query,
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_total_query,
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_fireplace_query,
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_subjects_query,
            'arguments': get_argument_matrix(FAKE_TIMEFRAMES, ((10,), (25,)))
        }
    ]

    def handle(self, *args, **options):
        for config in self.query_configs:
            for index, arguments in enumerate(config['arguments']):

                query_fn = config['get_query']
                query = query_fn(*arguments)
                body = prepare_msearch_query(query)
                response = es.msearch(index=settings.TAZBOARD_ELASTIC_INDEX, body=body)
                with open(get_mock_filepath_for_query(query), 'w') as outfile:
                    outfile.write(json.dumps(response, indent=4))
                # put aside one sample for e2e tests
                if index == 0:
                    with open(get_mock_test_sample_path_for_query_function(query_fn), 'w') as outfile:
                        outfile.write(json.dumps(response, indent=4))

        with open(MOCK_CXML_PATH, 'w') as outfile:
            outfile.write(fetch_ressort_cxml(settings.TAZBOARD_ID_FIREPLACE_CXML))
