import logging
from datetime import timedelta

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .elastic_client import search_or_raise_api_exception
from .errors import BadElasticResponseException
from .queries.histogram import get_histogram_query
from .queries.constants import INTERVAL_10MINUTES
from .queries.referrer import get_referrer_query
from .queries.devices import get_devices_query
from .queries.subjects import get_subjects_query
from .queries.toplist import get_toplist_msids_query, get_toplist_query
from .queries.total import get_total_query
from .queries.fireplace import get_fireplace_query, get_fireplace_query_msids_hits
from .query_params import HistogramQuerySerializer, ReferrerQuerySerializer, ToplistQuerySerializer, \
    DevicesQuerySerializer, TotalQuerySerializer, SubjectQuerySerializer, FireplaceQuerySerializer
from .schema import AutoSchemaWithQuery
from .transformers import elastic_histogram_response_to_histogram_graph, elastic_toplist_response_to_toplist, \
    elastic_toplist_msid_response_to_toplist, elastic_referrer_response_to_referrer_data, \
    elastic_devices_response_to_devices_graph, elastic_total_response_total, \
    elastic_fireplace_response_to_fireplace, elastic_subjects_response_to_subjects_data, \
    elastic_fireplace_msid_hits_response_to_fireplace_msids_hits
from .serializers import HistogramSerializer, ReferrerSerializer, ToplistSerializer, DevicesSerializer, \
    TotalSerializer, SubjectSerializer, FireplaceSerializer, ToplistMsidSerializer, FireplaceMsidSerializer

logger = logging.getLogger(__name__)


class RedocView(TemplateView):
    def get(self, request, *args):
        return render(request, 'api/redoc.html')


if settings.TAZBOARD_MOCKS_ENABLED:
    try:
        from .tests.common import activate_global_elastic_mocks
    except ImportError:
        raise Exception('Test module is not available in production distribution')
    activate_global_elastic_mocks()


class APIView(GenericAPIView):
    """
    Extending the GenericAPIView to extend it with support for validated query params
    The variant described in DRF docs using filters is too much entangled with django models and
    actual filtering. We only want query parameters with validation and schema autogeneration
    which we can achieve with this class
    """
    schema = AutoSchemaWithQuery()
    query_params = None

    def initial(self, request, *args, **kwargs):
        super(APIView, self).initial(request, *args, **kwargs)
        if hasattr(self, 'query_serializer'):
            serializer = self.query_serializer(data=self.request.GET)
            serializer.is_valid(raise_exception=True)
            self.query_params = serializer.validated_data


class HistogramView(APIView):
    serializer_class = HistogramSerializer
    query_serializer = HistogramQuerySerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())
        subject_name = self.query_params.get('subject', None)
        msid = self.query_params.get('msid', None)
        interval = self.query_params.get('interval', INTERVAL_10MINUTES)
        es_query = get_histogram_query(min_date, max_date, msid=msid, subject=subject_name, interval=interval)

        response = search_or_raise_api_exception(es_query)
        serializer = self.serializer_class(
            data=elastic_histogram_response_to_histogram_graph(response, filter_last=True)
        )
        if not serializer.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer.errors))
            raise BadElasticResponseException()
        return Response(serializer.data)


class ReferrerView(APIView):
    serializer_class = ReferrerSerializer
    query_serializer = ReferrerQuerySerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())
        msid = self.query_params.get('msid', None)
        query = get_referrer_query(min_date, max_date, msid=msid)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            data=elastic_referrer_response_to_referrer_data(response)
        )
        if not serializer.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer.errors))
            raise BadElasticResponseException()
        return Response(serializer.data)


class ToplistView(APIView):
    serializer_class = ToplistSerializer
    query_serializer = ToplistQuerySerializer
    msid_serializer_class = ToplistMsidSerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())
        min_date_previous_interval = min_date - (max_date - min_date)
        limit = self.query_params.get('limit', 10)
        subject = self.query_params.get('subject', None)

        # Get msids for top X articles with their corresponding clicks (device fingerprint)
        query_msids = get_toplist_msids_query(min_date, max_date, limit, subject)
        response_msids = search_or_raise_api_exception(query_msids)
        serializer_msids = self.msid_serializer_class(
            data=elastic_toplist_msid_response_to_toplist(response_msids), many=True
        )
        if not serializer_msids.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer_msids.errors))
            logger.error('Raw elastic response: {}'.format(response_msids))
            logger.error('Transformer data: {}'.format(elastic_toplist_msid_response_to_toplist(response_msids)))
            raise BadElasticResponseException()

        # Get hits for previous time frame, devices and referrer for every msid in the topX list
        query_toplist = get_toplist_query(serializer_msids.data, min_date_previous_interval, min_date, max_date)
        response_toplist = search_or_raise_api_exception(query_toplist)
        serializer_toplist = self.serializer_class(
            data=elastic_toplist_response_to_toplist(response_toplist, serializer_msids.data)
        )
        if not serializer_toplist.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer_toplist.errors))
            logger.error('Raw elastic response: {}'.format(response_toplist))
            logger.error('Transformer data: {}'
                         .format(elastic_toplist_response_to_toplist(response_toplist, serializer_msids.data)))
            raise BadElasticResponseException()
        return Response(serializer_toplist.data)


class FireplaceView(APIView):
    msid_serializer_class = FireplaceMsidSerializer
    serializer_class = FireplaceSerializer
    query_serializer = FireplaceQuerySerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())

        # Get msids with their corresponding clicks (device fingerprint) for current time frame
        query_msids_hits = get_fireplace_query_msids_hits(min_date, max_date)
        response_msids_hits = search_or_raise_api_exception(query_msids_hits)
        serializer_msids = self.msid_serializer_class(
            data=elastic_fireplace_msid_hits_response_to_fireplace_msids_hits(response_msids_hits), many=True
        )
        if not serializer_msids.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer_msids.errors))
            logger.error('Raw elastic response: {}'.format(response_msids_hits))
            logger.error('Transformer data: {}'
                         .format(elastic_fireplace_msid_hits_response_to_fireplace_msids_hits(response_msids_hits)))
            raise BadElasticResponseException()

        # Get hits for previous time frame, devices and referrer for every msid in the fireplace
        query = get_fireplace_query(serializer_msids.data, min_date, max_date)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            data=elastic_fireplace_response_to_fireplace(response, serializer_msids.data)
        )
        if not serializer.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer.errors))
            logger.error('Raw elastic response: {}'.format(response))
            logger.error('Transformer data: {}'.format(elastic_fireplace_response_to_fireplace(response)))
            raise BadElasticResponseException()
        return Response(serializer.data)


class DevicesView(APIView):
    serializer_class = DevicesSerializer
    query_serializer = DevicesQuerySerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())
        msid = self.query_params.get('msid', None)
        query = get_devices_query(min_date, max_date, msid=msid)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            data=elastic_devices_response_to_devices_graph(response)
        )
        if not serializer.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer.errors))
            raise BadElasticResponseException()
        return Response(serializer.data)


class TotalView(APIView):
    serializer_class = TotalSerializer
    query_serializer = TotalQuerySerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())
        msid = self.query_params.get('msid', None)
        query = get_total_query(min_date, max_date, msid=msid)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            data=elastic_total_response_total(response)
        )
        if not serializer.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer.errors))
            raise BadElasticResponseException()
        return Response(serializer.data)


class SubjectsView(APIView):
    serializer_class = SubjectSerializer
    query_serializer = SubjectQuerySerializer

    def get(self, request, *args, **kwargs):
        min_date = self.query_params.get('min_date', timezone.now() - timedelta(days=1))
        max_date = self.query_params.get('max_date', timezone.now())
        limit = self.query_params.get('limit', 10)
        query = get_subjects_query(min_date, max_date, limit)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            data=elastic_subjects_response_to_subjects_data(response)
        )
        if not serializer.is_valid():
            logger.error('Unexpected response from elastic\n{}'.format(serializer.errors))
            raise BadElasticResponseException()
        return Response(serializer.data)
