from django.utils import timezone

from tazboard.api.queries.common import get_fingerprint_aggregation_with_ranges, \
    get_interval_filter_exclude_bots, get_devices_aggregation, get_referrer_aggregation, maybe_add_subject_filter
from tazboard.api.queries.constants import KEY_TOPLIST_AGGREGATION, \
    KEY_TIMEFRAME_AGGREGATION, KEY_TREND_AGGREGATION, KEY_METADATA_FIELD_MSID
from tazboard.api.queries.devices import get_devices_query
from tazboard.api.queries.referrer import get_referrer_query


def get_toplist_msids_query(min_date, max_date=timezone.now(), limit=10, subject=None):
    min_date_previous_interval = min_date - (max_date - min_date)
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
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, max_date, exists_msid=True)
    }
    maybe_add_subject_filter(subject, query)
    return query


def get_hits_previous_interval_msid(min_date_previous_interval, min_date, msid):
    query = {
        "aggs": {
            KEY_TOPLIST_AGGREGATION: {
                "terms": {
                    "field": "msid",
                },
                "aggs": {
                    KEY_TREND_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint"
                        }
                    }
                },
                "meta": {
                    KEY_METADATA_FIELD_MSID: msid
                }
            }
        },
        "size": '0',
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, min_date, msid=msid)
    }
    return query


def get_toplist_query(msids_hits, min_date_previous_interval, min_date, max_date):
    query = []
    for article in msids_hits['data']:
        query_hits_previous_interval = get_hits_previous_interval_msid(min_date_previous_interval, min_date, article['msid'])
        query_referrer_msid = get_referrer_query(min_date, max_date, article['msid'])
        query_devices_msid = get_devices_query(min_date, max_date, article['msid'])
        query.append(query_hits_previous_interval)
        query.append(query_referrer_msid)
        query.append(query_devices_msid)

    return query
