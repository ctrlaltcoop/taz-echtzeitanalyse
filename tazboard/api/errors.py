from enum import Enum

from django.conf import settings
from rest_framework.exceptions import APIException


class ErrorCode(Enum):
    ELASTIC_UNAVAILABLE = 'ELASTIC_UNAVAILABLE'
    MALFORMED_ELASTIC_QUERY = 'MALFORMED_ELASTIC_QUERY'
    MALFORMED_ELASTIC_RESPONSE = 'MALFORMED_ELASTIC_RESPONSE'


class ElasticUnavailableException(APIException):
    status_code = 503
    default_code = ErrorCode.ELASTIC_UNAVAILABLE
    default_detail = 'Upstream elastic server not reachable at {}:{}, check logs for further information'.format(
        settings.TAZBOARD_ELASTIC_HOST,
        settings.TAZBOARD_ELASTIC_PORT
    )


class BadElasticQueryException(APIException):
    status_code = 500
    default_code = ErrorCode.MALFORMED_ELASTIC_QUERY
    default_detail = 'Malformed query to elastic search, check logs for further information'


class BadElasticResponseException(APIException):
    status_code = 500
    default_code = ErrorCode.MALFORMED_ELASTIC_RESPONSE
    default_detail = 'Malformed response from elastic, check logs for further information'
