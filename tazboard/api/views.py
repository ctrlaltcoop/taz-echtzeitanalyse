import logging
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .elastic_client import es, search_or_raise_api_exception
from .filters import ClickGraphFilterSet, ReferrerFilterSet, ToplistFilterSet
from .queries.constants import INTERVAL_10MINUTES
from .queries.referrer import get_referrer_query
from .queries.toplist import get_toplist_query
from .tests.common import get_elastic_mock_response
from .transformers import elastic_histogram_response_to_histogram_graph, elastic_referrer_response_to_referrer_graph, \
    elastic_toplist_response_to_toplist
from .queries.histogram import get_histogram_query
from .serializers import HistogramSerializer, ReferrerSerializer, ToplistSerializer

logger = logging.getLogger(__name__)


class RedocView(TemplateView):
    def get(self, request, *args):
        return render(request, 'api/redoc.html')


if settings.TAZBOARD_MOCKS_ENABLED:
    es.search = get_elastic_mock_response


class HistogramView(GenericAPIView):
    serializer_class = HistogramSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClickGraphFilterSet

    def get(self, request, *args, **kwargs):
        min_date = request.query_params.get('min', 'now-24h')
        max_date = request.query_params.get('max', 'now')
        msid = request.query_params.get('msid', None)
        interval = request.query_params.get('interval', INTERVAL_10MINUTES)
        es_query = get_histogram_query(min_date, max_date, msid=msid, interval=interval)

        response = search_or_raise_api_exception(es_query)
        serializer = self.serializer_class(
            elastic_histogram_response_to_histogram_graph(response)
        )
        return Response(serializer.data)


class ReferrerView(GenericAPIView):
    serializer_class = ReferrerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReferrerFilterSet

    def get(self, request, *args, **kwargs):
        min_date = request.query_params.get('min', 'now-24h')
        max_date = request.query_params.get('max', 'now')
        msid = request.query_params.get('msid', None)
        query = get_referrer_query(min_date, max_date, msid=msid)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            elastic_referrer_response_to_referrer_graph(response)
        )
        return Response(serializer.data)


class ToplistView(GenericAPIView):
    serializer_class = ToplistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ToplistFilterSet

    def get(self, request, *args, **kwargs):
        min_date = request.query_params.get('min', 'now-24h')
        max_date = request.query_params.get('max', 'now')
        limit = request.query_params.get('limit', 10)
        query = get_toplist_query(min_date, max_date, limit)
        response = search_or_raise_api_exception(query)
        serializer = self.serializer_class(
            elastic_toplist_response_to_toplist(response)
        )
        return Response(serializer.data)
