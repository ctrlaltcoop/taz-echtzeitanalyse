import logging

from django.conf import settings
from elasticsearch import Elasticsearch, RequestsHttpConnection, RequestError, ConnectionError, TransportError

from rest_framework.utils import json

from tazboard.api.errors import BadElasticQueryException, ElasticUnavailableException
from tazboard.api.utils.msearch_queries import prepare_msearch_query

# Get an instance of a logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ELASTIC_SEARCH_TIMEOUT = 45

es = Elasticsearch(
    hosts=[{'host': settings.TAZBOARD_ELASTIC_HOST, 'port': settings.TAZBOARD_ELASTIC_PORT}],
    use_ssl=settings.TAZBOARD_ELASTIC_SSL,
    verify_certs=settings.TAZBOARD_ELASTIC_VERIFY_CERT,
    ssl_show_warn=settings.TAZBOARD_ELASTIC_SHOW_SSL_WARN,
    connection_class=RequestsHttpConnection,
    timeout=ELASTIC_SEARCH_TIMEOUT,
)


def search_or_raise_api_exception(query, query_indices=None, local_logger=logger):
    # use msearch to send more than one query to the ES
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-multi-search.html
    # https://elasticsearch-py.readthedocs.io/en/v7.15.1/api.html#elasticsearch.Elasticsearch.msearch
    #
    # if query is an array, the response is an array too.
    # the response for query[0] is in result[0] (results in order/aligned with queries)

    # make every query a list, but keep original query as reference for resulttype

    body = prepare_msearch_query(query, query_indices)

    try:
        result = es.msearch(index=settings.TAZBOARD_ELASTIC_INDEX, body=body)
        local_logger.info('Successful elastic msearch query: \n{}'.format(body))
        if isinstance(query, list):
            return result['responses']
        else:
            return result['responses'][0]
    except RequestError as e:
        local_logger.error(
            'Bad request sent to elastic {}\n'
            'Dumping error info: {}\n'
            'Dumping executed query: {}\n'.format(
                e.error,
                json.dumps(e.info, indent=4),
                body
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
                body
            ))
        raise BadElasticQueryException()
