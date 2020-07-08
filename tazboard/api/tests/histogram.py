import os
import json
from datetime import timedelta

from unittest.mock import MagicMock, patch, Mock

from django.test import LiveServerTestCase
from django.utils import timezone
from elasticsearch import ConnectionError, RequestError

from tazboard.api.queries.constants import INTERVAL_10MINUTES, MOCK_FAKE_NOW
from tazboard.api.queries.histogram import get_histogram_query
from tazboard.api.tests.common import get_mock_test_sample_path_for_query_function

TEST_PATH = os.path.dirname(os.path.abspath(__file__))


class HistogramTestCase(LiveServerTestCase):

    def setUp(self):
        self.patcher = patch('tazboard.api.elastic_client.es')
        self.es_client = self.patcher.start()
        with open(get_mock_test_sample_path_for_query_function(get_histogram_query), 'r') as mock_response_file:
            self.es_client.search = MagicMock(return_value=json.load(mock_response_file))

    def test_histogram_response(self):
        min_date = (timezone.now() - timedelta(days=1))
        response = self.client.get('/api/v1/histogram', {
            'min_date': min_date.isoformat()
        })
        data = response.json()
        self.assertIn('data', data)
        self.assertIn('total', data)
        self.assertGreater(data['total'], 0)
        self.assertEqual(response.status_code, 200)

    @patch('tazboard.api.views.get_histogram_query')
    def test_histogram_query_only_timeframe(self, get_histogram_query_spy):
        min_date = timezone.now() - timedelta(days=1)
        max_date = timezone.now()
        self.client.get('/api/v1/histogram', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat()
        })
        self.es_client.search.assert_called_once()
        get_histogram_query_spy.assert_called_once()
        get_histogram_query_spy.assert_called_with(min_date, max_date, msid=None, interval=INTERVAL_10MINUTES)

    @patch('tazboard.api.views.get_histogram_query')
    def test_unfiltered_histogram_query_specify_msid(self, get_histogram_query):
        msid = '5555'
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.client.get('/api/v1/histogram', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
            'msid': msid
        })
        self.es_client.search.assert_called_once()
        get_histogram_query.assert_called_once()
        get_histogram_query.assert_called_with(min_date, max_date, msid=int(msid), interval=INTERVAL_10MINUTES)

    @patch('tazboard.api.views.get_histogram_query')
    def test_histogram_specify_interval(self, get_histogram_query_spy):
        interval = '25m'
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        response = self.client.get('/api/v1/histogram', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
            'interval': interval
        })
        self.assertEquals(response.status_code, 200)
        self.es_client.search.assert_called_once()
        get_histogram_query_spy.assert_called_once()
        get_histogram_query_spy.assert_called_with(min_date, max_date, msid=None, interval=interval)

    def test_expect_503_if_elastic_is_unavailable(self):
        self.es_client.search = Mock(side_effect=ConnectionError())
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        response = self.client.get('/api/v1/histogram', {
            'min_date': min_date.isoformat()
        })
        self.assertEquals(response.status_code, 503)

    def test_expect_500_if_bad_elastic_query(self):
        self.es_client.search = Mock(side_effect=RequestError('kaboom', 'error', {}))
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        response = self.client.get('/api/v1/histogram', {
            'min_date': min_date.isoformat()
        })
        self.assertEquals(response.status_code, 500)
