from functools import reduce

from django.conf import settings

from tazboard.api.queries.common import get_dict_path_safe
from tazboard.api.queries.constants import KEY_TIMESTAMP_AGGREGATION, KEY_FINGERPRINT_AGGREGATION, \
    KEY_REFERRER_AGGREGATION, KEY_TOPLIST_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_DEVICES_AGGREGATION, KEY_SUBJECTS_AGGREGATION, \
    KEY_ARTICLE_COUNT_AGGREGATION, KEY_METADATA_FIELD_MSID
from tazboard.api.queries.fireplace import get_fireplace_articles_msids
from tazboard.api.utils.list import get_index_or_none
from tazboard.api.utils.metadata import parse_article_metadata


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
        lambda acc, x: acc + x[KEY_TIMEFRAME_AGGREGATION]['value'],
        referrer_buckets, 0
    )
    return [
        {
            'referrer': bucket['key'],
            'hits': bucket[KEY_TIMEFRAME_AGGREGATION]['value'],
            'percentage':
                bucket[KEY_TIMEFRAME_AGGREGATION]['value'] / total if total > 0 else 0
        }
        for bucket in referrer_buckets
    ]


def _transform_device_buckets(device_buckets):
    return [
        {
            'deviceclass': bucket['key'],
            'hits': bucket[KEY_TIMEFRAME_AGGREGATION]['value']
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


def elastic_toplist_response_to_toplist(es_response, msids_data):
    data = _responses_to_article_data(es_response, msids_data)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    total = reduce(lambda acc, x: acc + x['hits'], msids_data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def _responses_to_article_data(es_response, msids_data):
    article_data = {}
    frontpage_msids = get_fireplace_articles_msids()

    for entry in msids_data:
        msid = entry['msid']
        hits = entry['hits']

        headline, kicker, pubtime = parse_article_metadata(msid)
        url = '{}!{}/'.format(settings.TAZBOARD_TAZ_WEB_URL, msid)
        archive = False
        frontpage_index = get_index_or_none(frontpage_msids, msid)
        if headline is None:
            headline = url
            archive = True

        article_partial_data = {
            'msid': msid,
            'headline': headline,
            'url': url,
            'kicker': kicker,
            'pubdate': pubtime,
            'frontpage': msid in frontpage_msids,
            'archive': archive,
            'frontpage_position': frontpage_index + 1 if frontpage_index is not None else None,
            'hits': hits
        }
        article_data[msid] = article_partial_data

    for entry in es_response:
        aggregation = entry['aggregations']

        if KEY_TOPLIST_AGGREGATION in aggregation:
            msid = get_dict_path_safe(
                aggregation[KEY_TOPLIST_AGGREGATION], 'meta', KEY_METADATA_FIELD_MSID
            )
            if len(aggregation[KEY_TOPLIST_AGGREGATION]['buckets']) != 0:
                hits_previous = aggregation[KEY_TOPLIST_AGGREGATION]['buckets'][0][KEY_TREND_AGGREGATION]['value']
            else:
                hits_previous = 0
            article_data[msid]['hits_previous'] = hits_previous

        if KEY_REFERRER_AGGREGATION in aggregation:
            msid = get_dict_path_safe(
                aggregation[KEY_REFERRER_AGGREGATION], 'meta', KEY_METADATA_FIELD_MSID
            )
            referrers = _transform_referrer_buckets(aggregation[KEY_REFERRER_AGGREGATION]['buckets'])
            article_data[msid]['referrers'] = referrers

        if KEY_DEVICES_AGGREGATION in aggregation:
            msid = get_dict_path_safe(
                aggregation[KEY_DEVICES_AGGREGATION], 'meta', KEY_METADATA_FIELD_MSID
            )
            devices = _transform_device_buckets(aggregation[KEY_DEVICES_AGGREGATION]['buckets'])
            article_data[msid]['devices'] = devices

    return list(article_data.values())


def _toplist_msid_response_to_msids(article_buckets):
    msids_data = []
    for bucket in article_buckets:
        msid = get_dict_path_safe(bucket, 'key')
        hits = bucket[KEY_TIMEFRAME_AGGREGATION]['value']
        msid_hits = {
            'msid': msid,
            'hits': hits
        }
        msids_data.append(msid_hits)
    return msids_data


def elastic_toplist_msid_response_to_toplist(es_response):
    msids_data = []
    buckets = es_response['aggregations'][KEY_TOPLIST_AGGREGATION]['buckets']
    for bucket in buckets:
        msid = get_dict_path_safe(bucket, 'key')
        hits = bucket[KEY_TIMEFRAME_AGGREGATION]['value']
        msid_hits = {
            'msid': msid,
            'hits': hits
        }
        msids_data.append(msid_hits)
    return msids_data


def elastic_fireplace_response_to_fireplace(es_response, msids_data):
    data = _responses_to_article_data(es_response, msids_data)
    total = reduce(lambda acc, x: acc + x['hits'], data, 0)
    total_previous = reduce(lambda acc, x: acc + x['hits_previous'], data, 0)
    return {
        'total': total,
        'total_previous': total_previous,
        'data': data
    }


def elastic_fireplace_msid_hits_response_to_fireplace_msids_hits(response_msids_hits):
    msids_data = []

    for entry in response_msids_hits:
        aggregation = entry['aggregations']
        msid = get_dict_path_safe(
            aggregation[KEY_TOPLIST_AGGREGATION], 'meta', KEY_METADATA_FIELD_MSID
        )
        hits = aggregation[KEY_TOPLIST_AGGREGATION]['buckets'][0][KEY_TREND_AGGREGATION]['value']
        msid_hits = {
            'msid': msid,
            'hits': hits
        }
        msids_data.append(msid_hits)

    return msids_data


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
