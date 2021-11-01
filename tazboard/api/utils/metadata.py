import requests

from xml.etree import ElementTree
from cachetools import cached, TTLCache
from django.conf import settings
from datetime import datetime


def fetch_article_cxml(msid):
    response = requests.get(
        'http://{cxml_host}/!{msid}/c.xml'.format(cxml_host=settings.TAZBOARD_CXML_ARTICLE_HOST, msid=msid),
        headers={
            'X-Forwarded-Host': settings.TAZBOARD_CXML_XFORWARD_HEADER,
            'X-Forwarded-Server': settings.TAZBOARD_CXML_XFORWARD_HEADER,
            'X-Forwarded-For': settings.TAZBOARD_CXML_XFORWARD_HEADER,
            'User-Agent': settings.TAZBOARD_CXML_USER_AGENT
        }
    )

    return response.text


@cached(cache=TTLCache(ttl=120, maxsize=float('inf')))
def parse_article_metadata(msid):
    try:
        xml_data = ElementTree.fromstring(fetch_article_cxml(msid))
        article_xml = xml_data.find('item')

        headline_tag = article_xml.find('headline')
        kicker_tag = article_xml.find('kicker')
        kicker = kicker_tag.text if (kicker_tag is not None) else None
        headline = headline_tag.text if (headline_tag is not None) else None

        xml_pubtime = article_xml.find('meta/published')
        tz = xml_pubtime.find('dt').get('tz')
        year = xml_pubtime.find('dt/y').text
        month = xml_pubtime.find('dt/mon').text
        day = xml_pubtime.find('dt/day').text
        hour = xml_pubtime.find('dt/h').text
        minute = xml_pubtime.find('dt/min').text
        second = xml_pubtime.find('dt/sec').text

        pubtime = datetime.strptime('{}-{}-{}T{}:{}:{}Z{}'.format(year, month, day, hour, minute, second, tz),
                                    '%Y-%m-%dT%H:%M:%SZ%z')

    except ElementTree.ParseError as error:
        print('Error occurred on parsing article with msid: {}'.format(msid))
        print(error)
        headline = 'Metadaten des Artikels nicht Abrufbar: http://static.taz.de/!{msid}/c.xml'.format(msid=msid)
        kicker = None
        pubtime = None

    return headline, kicker, pubtime
