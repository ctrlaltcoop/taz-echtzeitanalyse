from django.utils import timezone

from tazboard.api.queries.common import get_interval_filter_exclude_bots, maybe_add_subject_filter, \
    get_hits_interval_msid
from tazboard.api.queries.constants import KEY_TOPLIST_AGGREGATION, KEY_TIMEFRAME_AGGREGATION
from tazboard.api.queries.devices import get_devices_query
from tazboard.api.queries.referrer import get_referrer_query


def get_toplist_msids_query(min_date, max_date=timezone.now(), limit=10, subject=None):
    query = {
        "aggs": {
            KEY_TOPLIST_AGGREGATION: {
                "terms": {
                    "field": "msid",
                    "order": {
                        KEY_TIMEFRAME_AGGREGATION: "desc"
                    },
                    "size": str(limit)
                },
                "aggs": {
                    KEY_TIMEFRAME_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint"
                        }
                    }
                }
            }
        },
        "size": '0',
        "query": get_interval_filter_exclude_bots(min_date, max_date, exists_msid=True)
    }
    maybe_add_subject_filter(subject, query)
    return query


def get_toplist_query(msids_hits, min_date, max_date):
    query = []
    min_date_previous_interval = min_date - (max_date - min_date)
    for article in msids_hits:
        query_hits_previous_interval = get_hits_interval_msid(min_date_previous_interval, min_date, article['msid'])
        query_referrer_msid = get_referrer_query(min_date, max_date, article['msid'])
        query_devices_msid = get_devices_query(min_date, max_date, article['msid'])
        query.append(query_hits_previous_interval)
        query.append(query_referrer_msid)
        query.append(query_devices_msid)

    return query
