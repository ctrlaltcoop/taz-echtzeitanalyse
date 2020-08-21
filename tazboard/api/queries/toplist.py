from django.utils import timezone

from tazboard.api.queries.common import get_fingerprint_aggregation_with_ranges, \
    get_interval_filter_exclude_bots, get_devices_aggregation, get_referrer_aggregation, maybe_add_subject_filter
from tazboard.api.queries.constants import KEY_TOPLIST_AGGREGTAION, \
    KEY_EXTRA_FIELDS_AGGREGATION, KEY_REFERRER_AGGREGATION, KEY_RANGES_AGGREGATION, KEY_DEVICES_AGGREGATION


def get_toplist_query(min_date, max_date=timezone.now(), limit=10, subject=None):
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
                                "include": ['bid', 'kicker', 'pubtime', 'msid']
                            }
                        }
                    },
                    KEY_RANGES_AGGREGATION: get_fingerprint_aggregation_with_ranges(
                        min_date_previous_interval, min_date, max_date
                    ),
                    KEY_DEVICES_AGGREGATION: get_devices_aggregation(),
                    KEY_REFERRER_AGGREGATION: get_referrer_aggregation()
                }
            }
        },
        "size": str(limit),
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, max_date)
    }
    maybe_add_subject_filter(subject, query)
    return query
