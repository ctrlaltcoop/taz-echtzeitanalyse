from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_RANGES_AGGREGATION, KEY_ARTICLE_COUNT_AGGREGATION, KEY_REFERRER_AGGREGATION, \
    KEY_DEVICES_AGGREGATION


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


def maybe_add_subject_filter(subject, query):
    if subject:
        subject_filter = {
            "match_phrase": {
                "schwerpunkte": {
                    "query": str(subject)
                }
            }
        }
        query['query']['bool']['filter'] = [subject_filter] + query['query']['bool']['filter']
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


def get_referrer_aggregation(limit=10):
    return {
        "terms": {
            "field": "referrerlabel",
            "order": {
                "_count": "desc"
            },
            "size": str(limit)
        },
        "aggs": {
            KEY_FINGERPRINT_AGGREGATION: {
                "cardinality": {
                    "field": "fingerprint",
                }
            }
        }
    }


def get_referrer_aggregation_with_ranges(interval_start, interval_mid, interval_end, limit=10):
    return {
        "terms": {
            "field": "referrerlabel",
            "order": {
                "_count": "desc"
            },
            "size": str(limit)
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


def get_interval_filter_exclude_bots_with_msids(interval_start, interval_end, msids):
    base_query = get_interval_filter_exclude_bots(interval_start, interval_end)

    msid_query = {
        "terms": {
            "msid": msids
        }
    }
    base_query["bool"]["filter"].append(msid_query)
    return base_query


def get_devices_aggregation(limit=10):
    return {
        "terms": {
            "field": "deviceclass",
            "order": {
                "_count": "desc"
            },
            "size": str(limit)
        },
        "aggs": {
            KEY_FINGERPRINT_AGGREGATION: {
                "cardinality": {
                    "field": "fingerprint"
                }
            }
        }
    }


def get_subject_aggregation(limit=10):
    return {
        "terms": {
            "field": "schwerpunkte",
            "order": {
                "_count": "desc"
            },
            "size": str(limit)
        },
        "aggs": {
            KEY_FINGERPRINT_AGGREGATION: {
                "cardinality": {
                    "field": "fingerprint",
                }
            },
            KEY_ARTICLE_COUNT_AGGREGATION: {
                "cardinality": {
                    "field": "msid",
                }
            },
            KEY_REFERRER_AGGREGATION: get_referrer_aggregation(),
            KEY_DEVICES_AGGREGATION: get_devices_aggregation()
        }
    }
