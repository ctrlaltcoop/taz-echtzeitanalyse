from functools import reduce

from tazboard.api.queries.common import get_dict_path_safe
from tazboard.api.queries.constants import KEY_TIMESTAMP_AGGREGATION, KEY_FINGERPRINT_AGGREGATION, \
    KEY_REFERRER_AGGREGATION, KEY_TOPLIST_AGGREGTAION, KEY_RANGES_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_EXTRA_FIELDS_AGGREGATION, KEY_DEVICES_AGGREGATION


def _transform_ranges(buckets):
    data = {}
    for bucket in buckets:
        if bucket['key'] == KEY_TIMEFRAME_AGGREGATION:
            data['hits'] = bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        elif bucket['key'] == KEY_TREND_AGGREGATION:
            data['hits_previous'] = bucket[KEY_FINGERPRINT_AGGREGATION]['value']

    return data


def _transform_referrer_with_ranges_buckets(referrer_buckets):
    data = []
    total = 0
    total_previous = 0
    for referrer_bucket in referrer_buckets:
        hits_data = _transform_ranges(referrer_bucket[KEY_RANGES_AGGREGATION]['buckets'])
        total += hits_data['hits']
        total_previous += hits_data['hits_previous']
        referrer_data = {
            'referrertag': referrer_bucket['key'],
            **hits_data
        }
        data.append(referrer_data)
    for referrer in data:
        referrer['percentage'] = (referrer['hits'] / total) if total > 0 else 0
        referrer['percentage_previous'] = (referrer['hits_previous'] / total_previous) if total_previous > 0 else 0

    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def _transform_referrer_buckets(referrer_buckets):
    total = reduce(lambda acc, x: acc + x[KEY_FINGERPRINT_AGGREGATION]['value'], referrer_buckets, 0)
    return [
        {
            'referrer': bucket['key'],
            'hits': bucket[KEY_FINGERPRINT_AGGREGATION]['value'],
            'percentage': bucket[KEY_FINGERPRINT_AGGREGATION]['value'] / total
        }
        for bucket in referrer_buckets
    ]


def _transform_device_buckets(device_buckets):
    return [
        {
            'deviceclass': bucket['key'],
            'hits': bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        }
        for bucket in device_buckets
    ]


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


def elastic_toplist_response_to_toplist(es_response):
    data = []

    for toplist_bucket in es_response['aggregations'][KEY_TOPLIST_AGGREGTAION]['buckets']:
        if toplist_bucket['key'] == '__missing__':
            continue
        toplist_data = {
            'headline': toplist_bucket['key'],
            'kicker': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'kicker'
            ),
            'pubdate': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'pubtime'
            ),
            'msid': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'msid'
            ),
            'referrers': _transform_referrer_buckets(toplist_bucket[KEY_REFERRER_AGGREGATION]['buckets']),
            'devices': _transform_device_buckets(toplist_bucket[KEY_DEVICES_AGGREGATION]['buckets']),
            **_transform_ranges(toplist_bucket[KEY_RANGES_AGGREGATION]['buckets'])
        }
        data.append(toplist_data)
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def elastic_referrer_response_to_referrer_data(es_response):
    data = _transform_referrer_buckets(es_response['aggregations'][KEY_REFERRER_AGGREGATION]['buckets'])
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    return {
        'total': total,
        'data': data
    }


def elastic_devices_response_to_devices_graph(es_response):
    data = _transform_device_buckets(es_response['aggregations'][KEY_DEVICES_AGGREGATION]['buckets'])
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    return {
        'total': total,
        'data': data
    }
