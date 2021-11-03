import logging

from django.conf import settings
from elasticsearch import Elasticsearch, RequestsHttpConnection, RequestError, ConnectionError, TransportError

# Get an instance of a logger
from rest_framework.utils import json

from tazboard.api.errors import BadElasticQueryException, ElasticUnavailableException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ELASTIC_SEARCH_TIMEOUT = 45

es = Elasticsearch(
    hosts=[{'host': settings.TAZBOARD_ELASTIC_HOST, 'port': settings.TAZBOARD_ELASTIC_PORT}],
    use_ssl=settings.TAZBOARD_ELASTIC_SSL,
    verify_certs=settings.TAZBOARD_ELASTIC_VERIFY_CERT,
    connection_class=RequestsHttpConnection,
    timeout=ELASTIC_SEARCH_TIMEOUT,
)


def search_or_raise_api_exception(query, local_logger=logger):
    try:
        local_logger.info('Successful elastic query: {}'.format(query))
        return es.search(index=settings.TAZBOARD_ELASTIC_INDEX, body=query)
    except RequestError as e:
        local_logger.error(
            'Bad request sent to elastic {}\n'
            'Dumping error info: {}\n'
            'Dumping executed query: {}\n'.format(
                e.error,
                json.dumps(e.info, indent=4),
                query
            ))
        raise BadElasticQueryException()
    except ConnectionError:
        local_logger.error('Elasticsearch server not reachable', exc_info=True)
        raise ElasticUnavailableException()
    except TransportError as e:
        local_logger.error(
            'Bad request sent to elastic {}\n'
            'Dumping error info: {}\n'
            'Dumping executed query: {}\n'.format(
                e.error,
                json.dumps(e.info, indent=4),
                query
            ))
        raise BadElasticQueryException()
