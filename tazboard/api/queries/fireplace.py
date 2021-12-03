import requests

from xml.etree import ElementTree
from cachetools import cached, TTLCache
from random import randrange
from django.utils import timezone
from django.conf import settings
from tazboard.api.queries.common import get_fingerprint_aggregation_with_ranges, \
    get_interval_filter_exclude_bots_with_msids, get_devices_aggregation, get_referrer_aggregation, \
    get_hits_interval_msid
from tazboard.api.queries.constants import KEY_FIREPLACE_AGGREGATION, \
    KEY_EXTRA_FIELDS_AGGREGATION, KEY_REFERRER_AGGREGATION, KEY_DEVICES_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_FINGERPRINT_AGGREGATION
from tazboard.api.queries.devices import get_devices_query
from tazboard.api.queries.referrer import get_referrer_query


@cached(cache=TTLCache(ttl=randrange(90, 120), maxsize=float('inf')))
def fetch_ressort_cxml(pid):
    response = requests.get(
        'https://{}/!p{}/c.xml'.format(settings.TAZBOARD_CXML_HOST, pid),
        headers={
            'X-Forwarded-Host': settings.TAZBOARD_CXML_XFORWARD_HEADER,
            'X-Forwarded-Server': settings.TAZBOARD_CXML_XFORWARD_HEADER,
            'X-Forwarded-For': settings.TAZBOARD_CXML_XFORWARD_HEADER,
            'User-Agent': settings.TAZBOARD_CXML_USER_AGENT
        }
    )

    return response.text


def get_fireplace_articles_msids():
    xml_data = ElementTree.fromstring(fetch_ressort_cxml(settings.TAZBOARD_ID_FIREPLACE_CXML))
    articles = xml_data.findall("./directory/list/item/meta/id[@scope='cms-article']")
    fireplace_article_msids = [int(article.text) for article in articles[:settings.TAZBOARD_NUMBER_FIREPLACE_POSITIONS]]
    return fireplace_article_msids


def get_fireplace_query_msids_hits(min_date, max_date):
    fireplace_msids = get_fireplace_articles_msids()
    query = []

    for msid in fireplace_msids:
        query_hits_current_interval = get_hits_interval_msid(min_date, max_date, msid)
        query.append(query_hits_current_interval)

    return query


def get_fireplace_query(msids_hits, min_date, max_date=timezone.now()):
    min_date_previous_interval = min_date - (max_date - min_date)
    query = []

    for article in msids_hits:
        query_hits_previous_interval = get_hits_interval_msid(min_date_previous_interval, min_date, article['msid'])
        query_referrer_msid = get_referrer_query(min_date, max_date, article['msid'])
        query_devices_msid = get_devices_query(min_date, max_date, article['msid'])
        query.append(query_hits_previous_interval)
        query.append(query_referrer_msid)
        query.append(query_devices_msid)

    return query
