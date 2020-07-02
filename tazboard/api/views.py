from django.shortcuts import render
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .elastic_client import es
from .filters import ClickGraphFilterSet, ReferrerFilterSet
from .queries.constants import INTERVAL_10MINUTES
from .queries.referrer import get_referrer_query
from .transformers import elastic_histogram_response_to_histogram_graph, elastic_referrer_response_to_referrer_graph
from .queries.histogram import get_histogram_query
from .serializers import HistogramSerializer, ReferrerSerializer


class RedocView(TemplateView):
    def get(self, request, *args):
        return render(request, 'api/redoc.html')


class HistogramView(GenericAPIView):
    serializer_class = HistogramSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClickGraphFilterSet

    def get(self, request, *args, **kwargs):
        min_date = request.query_params.get('min', 'now-24h')
        max_date = request.query_params.get('max', 'now')
        msid = request.query_params.get('msid', None)
        interval = request.query_params.get('interval', INTERVAL_10MINUTES)
        response = es.search(body=get_histogram_query(min_date, max_date, msid=msid, interval=interval))
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
        response = es.search(body=get_referrer_query(min_date, max_date, msid=msid))
        serializer = self.serializer_class(
            elastic_referrer_response_to_referrer_graph(response)
        )
        return Response(serializer.data)
