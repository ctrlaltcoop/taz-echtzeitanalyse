from django.utils import timezone
from rest_framework.fields import DateTimeField, IntegerField, CharField
from rest_framework.serializers import Serializer

from tazboard.api.queries.constants import INTERVAL_10MINUTES


class HistogramQuerySerializer(Serializer):
    min_date = DateTimeField(required=True)
    max_date = DateTimeField(default=timezone.now())
    interval = CharField(default=INTERVAL_10MINUTES)
    msid = IntegerField(required=False)


class ReferrerQuerySerializer(Serializer):
    min_date = DateTimeField(required=True)
    max_date = DateTimeField(default=timezone.now())
    msid = IntegerField(required=False)


class ToplistQuerySerializer(Serializer):
    min_date = DateTimeField(required=True)
    max_date = DateTimeField(default=timezone.now())
    limit = IntegerField(default=10)


class TotalQuerySerializer(Serializer):
    min_date = DateTimeField(required=True)
    max_date = DateTimeField(default=timezone.now())


class DevicesQuerySerializer(Serializer):
    min_date = DateTimeField(required=True)
    max_date = DateTimeField(default=timezone.now())
    msid = IntegerField(required=False)
