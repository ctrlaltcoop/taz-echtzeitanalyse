import logging
from django.conf import settings
from elasticsearch import Elasticsearch, RequestsHttpConnection

# Get an instance of a logger
logger = logging.getLogger(__name__)


es = Elasticsearch(
    hosts=[{'host': settings.TAZBOARD_ELASTIC_HOST, 'port': settings.TAZBOARD_ELASTIC_PORT}],
    use_ssl=settings.TAZBOARD_ELASTIC_SSL,
    verify_certs=settings.TAZBOARD_ELASTIC_VERIFY_CERT,
    connection_class=RequestsHttpConnection
)
