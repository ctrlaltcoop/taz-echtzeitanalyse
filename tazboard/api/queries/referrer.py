from tazboard.api.queries.common import maybe_add_msid_filter
from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_REFERRER_AGGREGATION


def get_referrer_query(min_date, max_date='now', msid=None):
    query = {
        "aggs": {
            KEY_REFERRER_AGGREGATION: {
                "terms": {
                    "field": "referrerclass",
                    "order": {
                        "_count": "desc"
                    },
                    "size": 10
                },
                "aggs": {
                    KEY_FINGERPRINT_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint"
                        }
                    }
                }
            }
        },
        "size": 0,
        "docvalue_fields": [
            {
                "field": "@timestamp",
                "format": "date_time"
            }
        ],
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": min_date,
                                "lte": max_date
                            }
                        }
                    }
                ],
                "must_not": [
                    {
                        "match_phrase": {
                            "reloaded": "true"
                        }
                    },
                    {
                        "match_phrase": {
                            "tazlocal": "true"
                        }
                    },
                    {
                        "match_phrase": {
                            "device": {
                                "query": "Spider"
                            }
                        }
                    }
                ]
            }
        }
    }
    query = maybe_add_msid_filter(msid, query)
    return query
