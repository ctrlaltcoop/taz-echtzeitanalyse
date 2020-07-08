from functools import reduce

from tazboard.api.queries.common import get_dict_path_safe
from tazboard.api.queries.constants import KEY_TIMESTAMP_AGGREGATION, KEY_FINGERPRINT_AGGREGATION, \
    KEY_REFERRER_AGGREGATION, KEY_TOPLIST_AGGREGTAION, KEY_RANGES_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_EXTRA_FIELDS_AGGREGATION


def elastic_histogram_response_to_histogram_graph(es_response):
    data = [
        {
            'datetime': bucket['key_as_string'],
            'hits': bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        }
        for bucket in es_response['aggregations'][KEY_TIMESTAMP_AGGREGATION]['buckets']
    ]
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    return {
        'total': total,
        'data': data
    }


def _transform_referrer_buckets(referrer_buckets):
    data = []
    for referrer_bucket in referrer_buckets:
        referrer_data = {
            'referrerclass': referrer_bucket['key']
        }
        for timeframe_bucket in referrer_bucket[KEY_RANGES_AGGREGATION]['buckets']:
            if timeframe_bucket['key'] == KEY_TIMEFRAME_AGGREGATION:
                referrer_data['hits'] = timeframe_bucket[KEY_FINGERPRINT_AGGREGATION]['value']
            elif timeframe_bucket['key'] == KEY_TREND_AGGREGATION:
                referrer_data['hits_previous'] = timeframe_bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        data.append(referrer_data)
    return data


def elastic_referrer_response_to_referrer_graph(es_response):
    data = _transform_referrer_buckets(es_response['aggregations'][KEY_REFERRER_AGGREGATION]['buckets'])
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def elastic_toplist_response_to_toplist(es_response):
    data = []
    for toplist_bucket in es_response['aggregations'][KEY_TOPLIST_AGGREGTAION]['buckets']:
        toplist_data = {
            'headline': toplist_bucket['key'],
            'kicker': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'kicker'
            ),
            'referrers': _transform_referrer_buckets(toplist_bucket[KEY_REFERRER_AGGREGATION]['buckets'])
        }
        for timeframe_bucket in toplist_bucket[KEY_RANGES_AGGREGATION]['buckets']:
            if timeframe_bucket['key'] == KEY_TIMEFRAME_AGGREGATION:
                toplist_data['hits'] = timeframe_bucket[KEY_FINGERPRINT_AGGREGATION]['value']
            elif timeframe_bucket['key'] == KEY_TREND_AGGREGATION:
                toplist_data['hits_previous'] = timeframe_bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        data.append(toplist_data)
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }
