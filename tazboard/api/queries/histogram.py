from django.utils import timezone

from tazboard.api.queries.common import maybe_add_msid_filter
from tazboard.api.queries.constants import INTERVAL_10MINUTES, KEY_FINGERPRINT_AGGREGATION, KEY_TIMESTAMP_AGGREGATION


def get_histogram_query(min_date, max_date=timezone.now(), msid=None, interval=INTERVAL_10MINUTES):
    query = {
        "aggs": {
            KEY_TIMESTAMP_AGGREGATION: {
                "date_histogram": {
                    "field": "@timestamp",
                    "fixed_interval": interval,
                    "time_zone": "Europe/Berlin",
                    "min_doc_count": 0,
                    "extended_bounds": {"min": min_date.isoformat(), "max": max_date.isoformat()}
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
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": min_date.isoformat()
                            }
                        }
                    }
                ],
                "must_not": [
                    {
                        "match_phrase": {
                            "reloaded": "true"
                        }
                    },
                    {
                        "match_phrase": {
                            "tazlocal": "true"
                        }
                    },
                    {
                        "match_phrase": {
                            "device": {
                                "query": "Spider"
                            }
                        }
                    }
                ]
            }
        }
    }
    query = maybe_add_msid_filter(msid, query)
    return query
