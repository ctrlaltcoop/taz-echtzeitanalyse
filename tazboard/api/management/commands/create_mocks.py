import json
import logging
from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand

from tazboard.api.elastic_client import es, search_or_raise_api_exception
from tazboard.api.queries.constants import MOCK_FAKE_NOW, MOCK_CXML_PATH
from tazboard.api.errors import BadElasticResponseException
from tazboard.api.queries.devices import get_devices_query
from tazboard.api.queries.histogram import get_histogram_query
from tazboard.api.queries.referrer import get_referrer_query
from tazboard.api.queries.subjects import get_subjects_query
from tazboard.api.queries.toplist import get_toplist_query, get_toplist_msids_query
from tazboard.api.queries.total import get_total_query
from tazboard.api.queries.fireplace import get_fireplace_query, fetch_ressort_cxml, get_fireplace_query_msids_hits
from tazboard.api.serializers import ToplistMsidSerializer, FireplaceMsidSerializer
from tazboard.api.transformers import elastic_toplist_msid_response_to_toplist, \
    elastic_fireplace_msid_hits_response_to_fireplace_msids_hits
from tazboard.api.tests.common import get_mock_filepath_for_query, get_mock_test_sample_path_for_query_function
from tazboard.api.utils.tazdatetime import round_to_seconds
from tazboard.api.utils.msearch_queries import prepare_msearch_query


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
    (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=7)), MOCK_FAKE_NOW),
    # Commented out for now, since large timeframes cause elastic to crash
    # (round_to_seconds(MOCK_FAKE_NOW - timedelta(days=30)), MOCK_FAKE_NOW)
)


def handle_fireplace_cxml():
    with open(MOCK_CXML_PATH, 'w') as outfile:
        outfile.write(fetch_ressort_cxml(settings.TAZBOARD_ID_FIREPLACE_CXML))


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
            'get_query': get_devices_query,
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_total_query,
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_subjects_query,
            'arguments': get_argument_matrix(FAKE_TIMEFRAMES, ((10,), (25,)))
        }
    ]

    query_1step_configs = [
        {
            'get_query': get_toplist_msids_query,
            'arguments': get_argument_matrix(FAKE_TIMEFRAMES, ((10,), (100,)))
        },
        {
            'get_query': get_fireplace_query_msids_hits,
            'arguments': FAKE_TIMEFRAMES
        },
    ]

    query_2step_configs = [
        {
            'get_query': get_toplist_query,
            'arguments': FAKE_TIMEFRAMES
        },
        {
            'get_query': get_fireplace_query,
            'arguments': FAKE_TIMEFRAMES
        }
    ]

    def handle(self, *args, **options):
        self.handle_queries()
        self.handle_1st_step_queries()
        self.handle_2nd_step_queries()
        handle_fireplace_cxml()

    # handle all queries except for toplist and fireplace
    def handle_queries(self):
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

    # handle 1st step of toplist/fireplace
    def handle_1st_step_queries(self):
        for config in self.query_1step_configs:
            for index, arguments in enumerate(config['arguments']):
                query_fn = config['get_query']
                query = query_fn(*arguments)
                response = search_or_raise_api_exception(query)
                with open(get_mock_filepath_for_query(query), 'w') as outfile:
                    outfile.write(json.dumps(response, indent=4))
                # put aside one sample for e2e tests
                if index == 0:
                    with open(get_mock_test_sample_path_for_query_function(query_fn), 'w') as outfile:
                        outfile.write(json.dumps(response, indent=4))

    # handle 2nd step of toplist/fireplace
    def handle_2nd_step_queries(self):
        for config in self.query_2step_configs:
            for index, arguments in enumerate(config['arguments']):
                query_fn = config['get_query']
                msids_hits = []

                if query_fn == get_toplist_query:
                    with open(get_mock_test_sample_path_for_query_function(get_toplist_msids_query)) as response_file:
                        response_msids = json.loads(response_file.read())
                        serializer_msids = ToplistMsidSerializer(
                            data=elastic_toplist_msid_response_to_toplist(response_msids), many=True
                        )
                        if not serializer_msids.is_valid():
                            logger.error('Unexpected response from elastic\n{}'.format(serializer_msids.errors))
                            logger.error('Raw elastic response: {}'.format(response_msids))
                            logger.error(
                                'Transformer data: {}'.format(elastic_toplist_msid_response_to_toplist(response_msids)))
                            raise BadElasticResponseException()
                        msids_hits = serializer_msids.data

                if query_fn == get_fireplace_query:
                    with open(get_mock_test_sample_path_for_query_function(get_fireplace_query_msids_hits)) \
                                                                                                    as response_file:
                        response_msids = json.loads(response_file.read())
                        serializer_msids = FireplaceMsidSerializer(
                            data=elastic_fireplace_msid_hits_response_to_fireplace_msids_hits(response_msids), many=True
                        )
                        if not serializer_msids.is_valid():
                            logger.error('Unexpected response from elastic\n{}'.format(serializer_msids.errors))
                            logger.error('Raw elastic response: {}'.format(response_msids))
                            logger.error(
                                'Transformer data: {}'.format(
                                    elastic_fireplace_msid_hits_response_to_fireplace_msids_hits(response_msids)
                                )
                            )
                            raise BadElasticResponseException()
                        msids_hits = serializer_msids.data

                arguments = list(arguments)
                arguments.insert(0, msids_hits)
                query = query_fn(*arguments)
                body = prepare_msearch_query(query)
                response = es.msearch(index=settings.TAZBOARD_ELASTIC_INDEX, body=body)
                with open(get_mock_filepath_for_query(query), 'w') as outfile:
                    outfile.write(json.dumps(response, indent=4))
                # put aside one sample for e2e tests
                if index == 0:
                    with open(get_mock_test_sample_path_for_query_function(query_fn), 'w') as outfile:
                        outfile.write(json.dumps(response, indent=4))
