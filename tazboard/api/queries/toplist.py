from django.utils import timezone

from tazboard.api.queries.common import FINGERPRINT_AGGREGATION_WITH_RANGES, REFERRER_AGGREGATION_WITH_RANGES, \
    QUERY_FILTER_EXCLUDE_BOTS_IN_INTERVAL
from tazboard.api.queries.constants import KEY_TOPLIST_AGGREGTAION, \
    KEY_EXTRA_FIELDS_AGGREGATION, KEY_REFERRER_AGGREGATION, KEY_RANGES_AGGREGATION


def get_toplist_query(min_date, max_date=timezone.now(), limit=10):
    min_date_previous_interval = min_date - (max_date - min_date)
    query = {
        "aggs": {
            KEY_TOPLIST_AGGREGTAION: {
                "terms": {
                    "field": "headline",
                    "order": {
                        "_count": "desc"
                    },
                    "missing": "__missing__",
                    "size": str(limit)
                },
                "aggs": {
                    KEY_EXTRA_FIELDS_AGGREGATION: {
                        "top_hits": {
                            "size": 1,
                            "_source": {
                                "include": ['kicker', 'pubtime']
                            }
                        }
                    },
                    KEY_RANGES_AGGREGATION: FINGERPRINT_AGGREGATION_WITH_RANGES(
                        min_date_previous_interval, min_date, max_date
                    ),
                    KEY_REFERRER_AGGREGATION: REFERRER_AGGREGATION_WITH_RANGES(
                        min_date_previous_interval, min_date, max_date
                    )
                }
            }
        },
        "size": 0,
        "query": QUERY_FILTER_EXCLUDE_BOTS_IN_INTERVAL(min_date_previous_interval, max_date)
    }
    return query
