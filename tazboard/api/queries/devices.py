from django.utils import timezone
from tazboard.api.queries.common import maybe_add_msid_filter, get_interval_filter_exclude_bots
from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_DEVICES_AGGREGATION


def get_devices_query(min_date, max_date=timezone.now(), msid=None):
    query = {
        "aggs": {
            KEY_DEVICES_AGGREGATION: {
                "terms": {
                    "field": "deviceclass",
                    "order": {
                        "_count": "desc"
                    },
                    "size": 10
                },
                "aggs": {
                    KEY_FINGERPRINT_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint"
                        }
                    }
                }
            }
        },
        "size": 0,
        "docvalue_fields": [
            {
                "field": "@timestamp",
                "format": "date_time"
            }
        ],
        "query": get_interval_filter_exclude_bots(min_date, max_date)
    }
    query = maybe_add_msid_filter(msid, query)
    return query
