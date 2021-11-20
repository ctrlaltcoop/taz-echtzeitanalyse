import json
import os
from datetime import timedelta

from unittest.mock import patch, Mock, MagicMock

from django.test import LiveServerTestCase
from elasticsearch import RequestError, ConnectionError

from tazboard.api.queries.constants import MOCK_FAKE_NOW
from tazboard.api.queries.subjects import get_subjects_query
from tazboard.api.tests.common import get_mock_test_sample_path_for_query_function

TEST_PATH = os.path.dirname(os.path.abspath(__file__))


class SubjectsTestCase(LiveServerTestCase):

    def setUp(self):
        self.patcher = patch('tazboard.api.elastic_client.es')
        self.es_client = self.patcher.start()
        with open(get_mock_test_sample_path_for_query_function(get_subjects_query), 'r') as mock_response_file:
            self.es_client.msearch = MagicMock(return_value=json.load(mock_response_file))
        self.patcher_msearch_utils = patch('tazboard.api.elastic_client.prepare_msearch_query')
        self.prepare_msearch_query = self.patcher_msearch_utils.start()
        self.prepare_msearch_query = MagicMock(return_value='{bla}')

    def tearDown(self):
        self.patcher.stop()
        self.patcher_msearch_utils.stop()

    def test_subjects_response(self):
        min_date = MOCK_FAKE_NOW - timedelta(minutes=10)
        max_date = MOCK_FAKE_NOW
        response = self.client.get('/api/v1/subjects', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
        })
        data = response.json()
        self.assertIn('data', data)
        self.assertGreater(len(data['data']), 0)
        self.assertEqual(response.status_code, 200)

    def test_subjects_400_without_timeframe(self):
        response = self.client.get('/api/v1/subjects')
        self.assertEqual(response.status_code, 400)

    @patch('tazboard.api.views.get_subjects_query')
    def test_subjects_with_limit(self, get_subjects_query_spy):
        min_date = MOCK_FAKE_NOW - timedelta(hours=24)
        max_date = MOCK_FAKE_NOW
        response = self.client.get('/api/v1/subjects', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
            'limit': 25
        })
        self.assertEquals(response.status_code, 200)
        self.es_client.msearch.assert_called_once()
        get_subjects_query_spy.assert_called_once()
        get_subjects_query_spy.assert_called_with(min_date, max_date, 25)

    def test_expect_503_if_elastic_is_unavailable(self):
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.es_client.msearch = Mock(side_effect=ConnectionError())
        response = self.client.get('/api/v1/subjects', {
            "min_date": min_date.isoformat(),
            "max_date": max_date.isoformat()
        })
        self.assertEquals(response.status_code, 503)

    def test_expect_500_if_bad_elastic_query(self):
        min_date = MOCK_FAKE_NOW - timedelta(days=1)
        max_date = MOCK_FAKE_NOW
        self.es_client.msearch = Mock(side_effect=RequestError('kaboom', 'error', {}))
        response = self.client.get('/api/v1/subjects', {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat()
        })
        self.assertEquals(response.status_code, 500)
