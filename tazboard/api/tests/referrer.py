import json
import os
from datetime import timedelta

from unittest.mock import patch, Mock, MagicMock

from django.test import LiveServerTestCase
from elasticsearch import RequestError, ConnectionError

from tazboard.api.queries.constants import MOCK_FAKE_NOW
from tazboard.api.queries.referrer import get_referrer_query
from tazboard.api.tests.common import get_mock_test_sample_path_for_query_function

TEST_PATH = os.path.dirname(os.path.abspath(__file__))


class ReferrerTestCase(LiveServerTestCase):

    def setUp(self):
        self.patcher = patch('tazboard.api.elastic_client.es')
        self.es_client = self.patcher.start()
        with open(get_mock_test_sample_path_for_query_function(get_referrer_query), 'r') as mock_response_file:
            self.es_client.msearch = MagicMock(return_value=json.load(mock_response_file))
        self.patcher_msearch_utils = patch('tazboard.api.elastic_client.prepare_msearch_query')
        self.prepare_msearch_query = self.patcher_msearch_utils.start()
        self.prepare_msearch_query = MagicMock(return_value='{bla}')

    def tearDown(self):
        self.patcher.stop()
        self.patcher_msearch_utils.stop()

    def test_referrer_query_correct_response(self):
        min_date = MOCK_FAKE_NOW - timedelta(minutes=10)
        max_date = MOCK_FAKE_NOW
        response = self.client.get('/api/v1/referrer', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
        })
        data = response.json()
        self.assertIn('data', data)
        self.assertIn('total', data)
        self.assertGreater(data['total'], 0)
        self.assertEqual(response.status_code, 200)

    @patch('tazboard.api.views.get_referrer_query')
    def test_referrer_query_only_timeframe(self, get_referrer_query_spy):
        min_date = MOCK_FAKE_NOW - timedelta(minutes=15)
        max_date = MOCK_FAKE_NOW
        response = self.client.get('/api/v1/referrer', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
        })
        self.assertEquals(response.status_code, 200)
        self.es_client.msearch.assert_called_once()
        get_referrer_query_spy.assert_called_once()
        get_referrer_query_spy.assert_called_with(min_date, max_date, msid=None)

    @patch('tazboard.api.views.get_referrer_query')
    def test_unfiltered_referrer_query_specify_msid(self, get_referrer_query_spy):
        min_date = MOCK_FAKE_NOW - timedelta(hours=24)
        max_date = MOCK_FAKE_NOW
        response = self.client.get('/api/v1/referrer', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
            'msid': '5555'
        })
        self.assertEquals(response.status_code, 200)
        self.es_client.msearch.assert_called_once()
        get_referrer_query_spy.assert_called_once()
        get_referrer_query_spy.assert_called_with(min_date, max_date, msid=5555)

    def test_expect_503_if_elastic_is_unavailable(self):
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.es_client.msearch = Mock(side_effect=ConnectionError())
        response = self.client.get('/api/v1/referrer', {
            "min_date": min_date.isoformat(),
            "max_date": max_date.isoformat()
        })
        self.assertEquals(response.status_code, 503)

    def test_expect_500_if_bad_elastic_query(self):
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.es_client.msearch = Mock(side_effect=RequestError('kaboom', 'error', {}))
        response = self.client.get('/api/v1/referrer', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat()
        })
        self.assertEquals(response.status_code, 500)
