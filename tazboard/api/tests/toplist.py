import json
import os
from datetime import timedelta

from unittest.mock import patch, Mock, MagicMock

from django.test import LiveServerTestCase
from elasticsearch import RequestError, ConnectionError

from tazboard.api.queries.constants import MOCK_FAKE_NOW
from tazboard.api.queries.toplist import get_toplist_query
from tazboard.api.tests.common import get_mock_test_sample_path_for_query_function

TEST_PATH = os.path.dirname(os.path.abspath(__file__))


class ToplistTestCase(LiveServerTestCase):

    def setUp(self):
        self.es_patcher = patch('tazboard.api.elastic_client.es')
        self.es_client = self.es_patcher.start()
        with open(get_mock_test_sample_path_for_query_function(get_toplist_query), 'r') as mock_response_file:
            self.es_client.msearch = MagicMock(return_value=json.load(mock_response_file))
        self.patcher_msearch_utils = patch('tazboard.api.elastic_client.prepare_msearch_query')
        self.prepare_msearch_query = self.patcher_msearch_utils.start()
        self.prepare_msearch_query = MagicMock(return_value='{bla}')

        self.cxml_patcher = patch('tazboard.api.transformers.get_article_metadata')
        self.cxml_parse_metadata = self.cxml_patcher.start()
        self.cxml_parse_metadata.return_value = ['Some Headline', 'Some Kicker', MOCK_FAKE_NOW]

    def tearDown(self):
        self.es_patcher.stop()
        self.cxml_patcher.stop()
        self.patcher_msearch_utils.stop()

    def test_toplist_400_without_timeframe(self):
        response = self.client.get('/api/v1/toplist')
        self.assertEqual(response.status_code, 400)

    def test_expect_503_if_elastic_is_unavailable(self):
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.es_client.msearch = Mock(side_effect=ConnectionError())
        response = self.client.get('/api/v1/toplist', {
            "min_date": min_date.isoformat(),
            "max_date": max_date.isoformat()
        })
        self.assertEquals(response.status_code, 503)

    def test_expect_500_if_bad_elastic_query(self):
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.es_client.msearch = Mock(side_effect=RequestError('kaboom', 'error', {}))
        response = self.client.get('/api/v1/toplist', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat()
        })
        self.assertEquals(response.status_code, 500)
