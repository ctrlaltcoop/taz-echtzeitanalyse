from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_TOPLIST_AGGREGTAION, \
    KEY_EXTRA_FIELDS_AGGREGATION, KEY_REFERRER_AGGREGATION


def get_toplist_query(min_date, max_date='now', limit='10'):
    query = {
        "aggs": {
            KEY_TOPLIST_AGGREGTAION: {
                "terms": {
                    "field": "headline",
                    "order": {
                        "_count": "desc"
                    },
                    "missing": "__missing__",
                    "size": limit
                },
                "aggs": {
                    KEY_EXTRA_FIELDS_AGGREGATION: {
                        "top_hits": {
                            "size": 1,
                            "_source": {
                                "include": ['kicker']
                            }
                        }
                    },
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
                    },
                    KEY_FINGERPRINT_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint"
                        }
                    }
                }
            }
        },
        "size": 0,
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
    return query
