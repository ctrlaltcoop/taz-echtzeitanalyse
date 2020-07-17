from django.utils import timezone

from tazboard.api.queries.common import get_fingerprint_aggregation_with_ranges, get_referrer_aggregation_with_ranges, \
    get_interval_filter_exclude_bots
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
                                "include": ['kicker', 'pubtime', 'msid']
                            }
                        }
                    },
                    KEY_RANGES_AGGREGATION: get_fingerprint_aggregation_with_ranges(
                        min_date_previous_interval, min_date, max_date
                    ),
                    KEY_REFERRER_AGGREGATION: get_referrer_aggregation_with_ranges(
                        min_date_previous_interval, min_date, max_date
                    )
                }
            }
        },
        "size": 0,
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, max_date)
    }
    return query
