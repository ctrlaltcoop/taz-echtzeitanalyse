from datetime import datetime

from django.utils.timezone import make_aware


KEY_FINGERPRINT_AGGREGATION = "2"
KEY_TIMESTAMP_AGGREGATION = "3"
KEY_REFERRER_AGGREGATION = "4"
KEY_TOPLIST_AGGREGTAION = "5"
KEY_EXTRA_FIELDS_AGGREGATION = "6"

INTERVAL_10MINUTES = '10m'


MOCK_FAKE_NOW = make_aware(datetime(year=2020, month=7, day=7))
