import requests

from xml.etree import ElementTree
from cachetools import cached, TTLCache
from django.utils import timezone
from django.conf import settings
from tazboard.api.queries.common import get_fingerprint_aggregation_with_ranges, \
    get_interval_filter_exclude_bots_with_msids, get_devices_aggregation, get_referrer_aggregation
from tazboard.api.queries.constants import KEY_FIREPLACE_AGGREGATION, \
    KEY_EXTRA_FIELDS_AGGREGATION, KEY_REFERRER_AGGREGATION, KEY_DEVICES_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_FINGERPRINT_AGGREGATION


@cached(cache=TTLCache(ttl=60, maxsize=float('inf')))
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
    fireplace_article_msids = [article.text for article in articles[:settings.TAZBOARD_NUMBER_FIREPLACE_POSITIONS]]
    return fireplace_article_msids


def get_fireplace_query(min_date, max_date=timezone.now()):
    fireplace_msids = get_fireplace_articles_msids()
    min_date_previous_interval = min_date - (max_date - min_date)
    query = {
        "aggs": {
            KEY_FIREPLACE_AGGREGATION: {
                "terms": {
                    "field": "msid",
                    "order": {
                        "{}>{}".format(KEY_TIMEFRAME_AGGREGATION, KEY_FINGERPRINT_AGGREGATION): "desc"
                    },
                    "missing": "__missing__"
                },
                "aggs": {
                    KEY_EXTRA_FIELDS_AGGREGATION: {
                        "top_hits": {
                            "size": 1,
                            "_source": {
                                "includes": ['bid', 'kicker', 'pubtime', 'msid', 'headline']
                            }
                        }
                    },
                    **get_fingerprint_aggregation_with_ranges(
                        min_date_previous_interval, min_date, max_date
                    ),
                    KEY_DEVICES_AGGREGATION: get_devices_aggregation(),
                    KEY_REFERRER_AGGREGATION: get_referrer_aggregation()
                }
            }
        },
        "size": 0,
        "query": get_interval_filter_exclude_bots_with_msids(min_date_previous_interval, max_date, fireplace_msids)
    }
    return query
