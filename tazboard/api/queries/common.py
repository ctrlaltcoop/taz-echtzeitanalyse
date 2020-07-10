from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_RANGES_AGGREGATION


def maybe_add_msid_filter(msid, query):
    if msid:
        msid_filter = {
            "match_phrase": {
                "msid": {
                    "query": str(msid)
                }
            }
        }
        query['query']['bool']['filter'] = [msid_filter] + query['query']['bool']['filter']
    return query


def get_dict_path_safe(obj: dict, *path_segments):
    head = obj
    for segment in path_segments:
        try:
            head = head[segment]
        except (KeyError, IndexError):
            return None
    return head


def get_fingerprint_aggregation_with_ranges(interval_start, interval_mid, interval_end):
    return {
        "range": {
            "field": "@timestamp",
            "ranges": [
                {
                    "key": KEY_TIMEFRAME_AGGREGATION,
                    "from": interval_mid.isoformat(),
                    "to": interval_end.isoformat()
                },
                {
                    "key": KEY_TREND_AGGREGATION,
                    "from": interval_start.isoformat(),
                    "to": interval_mid.isoformat()
                }
            ],
        },
        "aggs": {
            KEY_FINGERPRINT_AGGREGATION: {
                "cardinality": {
                    "field": "fingerprint",
                }
            }
        }
    }


def get_referrer_aggregation_with_ranges(interval_start, interval_mid, interval_end):
    return {
        "terms": {
            "field": "referrertags",
            "order": {
                "_count": "desc"
            },
            "size": 10
        },
        "aggs": {
            KEY_RANGES_AGGREGATION: {
                "range": {
                    "field": "@timestamp",
                    "ranges": [
                        {
                            "key": KEY_TIMEFRAME_AGGREGATION,
                            "from": interval_mid.isoformat(),
                            "to": interval_end.isoformat()
                        },
                        {
                            "key": KEY_TREND_AGGREGATION,
                            "from": interval_start.isoformat(),
                            "to": interval_mid.isoformat()
                        }
                    ],

                },
                "aggs": {
                    KEY_FINGERPRINT_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint",
                        }
                    }
                }
            },
        }
    }


def get_interval_filter_exclude_bots(interval_start, interval_end):
    return {
        "bool": {
            "filter": [
                {
                    "range": {
                        "@timestamp": {
                            "gte": interval_start.isoformat(),
                            "lte": interval_end.isoformat()
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
