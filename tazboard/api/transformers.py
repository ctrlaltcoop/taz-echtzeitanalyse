from functools import reduce

from django.conf import settings

from tazboard.api.queries.common import get_dict_path_safe
from tazboard.api.queries.constants import KEY_TIMESTAMP_AGGREGATION, KEY_FINGERPRINT_AGGREGATION, \
    KEY_REFERRER_AGGREGATION, KEY_TOPLIST_AGGREGTAION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_EXTRA_FIELDS_AGGREGATION, KEY_DEVICES_AGGREGATION, KEY_FIREPLACE_AGGREGATION, \
    KEY_SUBJECTS_AGGREGATION, KEY_ARTICLE_COUNT_AGGREGATION
from tazboard.api.queries.fireplace import get_fireplace_articles_msids
from tazboard.api.utils.list import get_index_or_none


def _transform_ranges(buckets):
    return {
        'hits': buckets[KEY_TIMEFRAME_AGGREGATION]['doc_count'],
        'hits_previous': buckets[KEY_TREND_AGGREGATION]['doc_count']
    }


def _transform_ranges_with_fingerprint_aggregation(buckets):
    return {
        'hits': buckets[KEY_TIMEFRAME_AGGREGATION][KEY_FINGERPRINT_AGGREGATION]['value'],
        'hits_previous': buckets[KEY_TREND_AGGREGATION][KEY_FINGERPRINT_AGGREGATION]['value']
    }


def _transform_ranges_for_total(buckets):
    return {
        'hits': buckets[KEY_TIMEFRAME_AGGREGATION]['doc_count'],
        'hits_previous': buckets[KEY_TREND_AGGREGATION]['doc_count']
    }


def _transform_referrer_with_ranges_buckets(referrer_buckets):
    data = []
    total = 0
    total_previous = 0
    for referrer_bucket in referrer_buckets:
        hits_data = _transform_ranges_with_fingerprint_aggregation(referrer_bucket)
        total += hits_data['hits']
        total_previous += hits_data['hits_previous']
        referrer_data = {
            'referrerlabel': referrer_bucket['key'],
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
    total = reduce(
        lambda acc, x: acc + x[KEY_TIMEFRAME_AGGREGATION]['doc_count'],
        referrer_buckets, 0
    )
    return [
        {
            'referrer': bucket['key'],
            'hits': bucket[KEY_TIMEFRAME_AGGREGATION]['doc_count'],
            'percentage':
                bucket[KEY_TIMEFRAME_AGGREGATION]['doc_count'] / total if total > 0 else 0
        }
        for bucket in referrer_buckets
    ]


def _transform_device_buckets(device_buckets):
    return [
        {
            'deviceclass': bucket['key'],
            'hits': bucket[KEY_TIMEFRAME_AGGREGATION]['doc_count']
        }
        for bucket in device_buckets
    ]


def _transform_subject_buckets(subject_buckets):
    return [
        {
            'subject_name': bucket['key'],
            'article_count': bucket[KEY_ARTICLE_COUNT_AGGREGATION]['value'],
            'hits': bucket[KEY_FINGERPRINT_AGGREGATION]['value'],
            'referrers': _transform_referrer_buckets(bucket[KEY_REFERRER_AGGREGATION]['buckets']),
            'devices': _transform_device_buckets(bucket[KEY_DEVICES_AGGREGATION]['buckets']),
        }
        for bucket in subject_buckets
    ]


def elastic_histogram_response_to_histogram_graph(es_response, filter_last=False):
    timestamp_buckets = es_response['aggregations'][KEY_TIMESTAMP_AGGREGATION]['buckets']
    # in date aggregations the last item is displaying an uncompleted interval not reflecting comparable data
    if filter_last:
        timestamp_buckets = timestamp_buckets[:-1]
    data = [
        {
            'datetime': bucket['key_as_string'],
            'hits': bucket[KEY_FINGERPRINT_AGGREGATION]['value']
        }
        for bucket in timestamp_buckets
    ]
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    return {
        'total': total,
        'data': data
    }


def _article_response_to_article_data(article_buckets):
    data = []
    frontpage_msids = get_fireplace_articles_msids()
    for toplist_bucket in article_buckets:
        headline = get_dict_path_safe(
            toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'headline'
        )
        msid = get_dict_path_safe(
            toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'msid'
        )
        url = '{}!{}/'.format(settings.TAZBOARD_TAZ_WEB_URL, msid)
        archive = False
        frontpage_index = get_index_or_none(frontpage_msids, msid)
        if headline is None:
            headline = url
            archive = True

        toplist_data = {
            'headline': headline,
            'url': url,
            'kicker': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'kicker'
            ),
            'pubdate': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'pubtime'
            ),
            'msid': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'msid'
            ),
            'bid': get_dict_path_safe(
                toplist_bucket, KEY_EXTRA_FIELDS_AGGREGATION, 'hits', 'hits', 0, '_source', 'bid'
            ),
            'referrers': _transform_referrer_buckets(toplist_bucket[KEY_REFERRER_AGGREGATION]['buckets']),
            'devices': _transform_device_buckets(toplist_bucket[KEY_DEVICES_AGGREGATION]['buckets']),
            'frontpage': msid in frontpage_msids,
            'archive': archive,
            'frontpage_position': frontpage_index + 1 if frontpage_index is not None else None,
            **_transform_ranges_with_fingerprint_aggregation(toplist_bucket)
        }
        data.append(toplist_data)
    return data


def elastic_toplist_response_to_toplist(es_response):
    data = _article_response_to_article_data(es_response['aggregations'][KEY_TOPLIST_AGGREGTAION]['buckets'])
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def elastic_fireplace_response_to_fireplace(es_response):
    data = _article_response_to_article_data(es_response['aggregations'][KEY_FIREPLACE_AGGREGATION]['buckets'])
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def elastic_total_response_total(es_response):
    data = _transform_ranges(es_response['aggregations'])
    return {
        'total': data['hits'],
        'total_previous': data['hits_previous'],
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


def elastic_subjects_response_to_subjects_data(es_response):
    data = _transform_subject_buckets(es_response['aggregations'][KEY_SUBJECTS_AGGREGATION]['buckets'])
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    return {
        'total': total,
        'data': data
    }
