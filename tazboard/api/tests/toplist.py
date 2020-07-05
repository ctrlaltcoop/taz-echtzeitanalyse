import os
import json

from unittest.mock import MagicMock, patch, Mock

from django.test import LiveServerTestCase
from elasticsearch import RequestError, ConnectionError

TEST_PATH = os.path.dirname(os.path.abspath(__file__))


class ToplistTestCase(LiveServerTestCase):

    def setUp(self):
        self.patcher = patch('tazboard.api.elastic_client.es')
        self.es_client = self.patcher.start()
        with open(os.path.join(TEST_PATH, 'mocks/toplist.json')) as mock_response:
            self.es_client.search = MagicMock(return_value=json.load(mock_response))

    def tearDown(self):
        self.patcher.stop()

    def test_unfiltered_histogram_response(self):
        response = self.client.get('/api/v1/toplist')
        data = response.json()
        self.assertIn('data', data)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()['data']), 0)

    @patch('tazboard.api.views.get_toplist_query')
    def test_unfiltered_histogram_query_only_timeframe(self, get_toplist_query):
        self.client.get('/api/v1/toplist?min=now-24h&max=now')
        self.es_client.search.assert_called_once()
        get_toplist_query.assert_called_once()
        get_toplist_query.assert_called_with('now-24h', 'now', 10)

    @patch('tazboard.api.views.get_toplist_query')
    def test_unfiltered_histogram_query_specify_msid(self, get_toplist_query):
        self.client.get('/api/v1/toplist?min=now-24h&max=now')
        self.es_client.search.assert_called_once()
        get_toplist_query.assert_called_once()
        get_toplist_query.assert_called_with('now-24h', 'now', 10)

    @patch('tazboard.api.views.get_toplist_query')
    def test_unfiltered_histogram_query_specify_interval(self, get_toplist_query):
        self.client.get('/api/v1/toplist?min=now-12h&max=now&limit=24')
        self.es_client.search.assert_called_once()
        get_toplist_query.assert_called_once()
        get_toplist_query.assert_called_with('now-12h', 'now', '24')

    def test_expect_503_if_elastic_is_unavailable(self):
        self.es_client.search = Mock(side_effect=ConnectionError())
        response = self.client.get('/api/v1/toplist')
        self.assertEquals(response.status_code, 503)

    def test_expect_500_if_bad_elastic_query(self):
        self.es_client.search = Mock(side_effect=RequestError('kaboom', 'error', {}))
        response = self.client.get('/api/v1/toplist')
        self.assertEquals(response.status_code, 500)
