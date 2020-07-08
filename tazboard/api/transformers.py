from functools import reduce

from tazboard.api.queries.constants import KEY_TIMESTAMP_AGGREGATION, KEY_FINGERPRINT_AGGREGATION, \
    KEY_REFERRER_AGGREGATION, KEY_TOPLIST_AGGREGTAION


def elastic_histogram_response_to_histogram_graph(es_response):
    data = [
        {
            'datetime': bucket['key_as_string'],
            'value': bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        }
        for bucket in es_response['aggregations'][KEY_TIMESTAMP_AGGREGATION]['buckets']
    ]
    total = reduce(lambda acc, x: acc + x['value'], data, 0)
    return {
        'total': total,
        'data': data
    }


def elastic_referrer_response_to_referrer_graph(es_response):
    data = [
        {
            'referrerclass': bucket['key'],
            'value': bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        }
        for bucket in es_response['aggregations'][KEY_REFERRER_AGGREGATION]['buckets']
    ]
    total = reduce(lambda acc, x: acc + x['value'], data, 0)
    return {
        'total': total,
        'data': data
    }


def elastic_toplist_response_to_toplist(es_response):
    data = [
        {
            'name': bucket['key'],
            'value': bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        }
        for bucket in es_response['aggregations'][KEY_TOPLIST_AGGREGTAION]['buckets']
    ]
    return {
        'data': data
    }
