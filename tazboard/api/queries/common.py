from tazboard.api.queries.constants import KEY_FINGERPRINT_AGGREGATION, KEY_TIMEFRAME_AGGREGATION, \
    KEY_TREND_AGGREGATION, KEY_ARTICLE_COUNT_AGGREGATION, KEY_REFERRER_AGGREGATION, \
    KEY_DEVICES_AGGREGATION, KEY_METADATA_FIELD_MSID, KEY_TOPLIST_AGGREGATION


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
        KEY_TIMEFRAME_AGGREGATION: {
            "filter": {
                "range": {
                    "@timestamp": {
                        "gte": interval_mid.isoformat(),
                        "lte": interval_end.isoformat()
                    },
                },
            },
            "aggs": {
                KEY_FINGERPRINT_AGGREGATION: {
                    "cardinality": {
                        "field": "fingerprint",
                    }
                }
            }
        },
        KEY_TREND_AGGREGATION: {
            "filter": {
                "range": {
                    "@timestamp": {
                        "gte": interval_start.isoformat(),
                        "lte": interval_mid.isoformat()
                    },
                },
            },
            "aggs": {
                KEY_FINGERPRINT_AGGREGATION: {
                    "cardinality": {
                        "field": "fingerprint",
                    }
                }
            }
        }
    }


def get_ranges(interval_start, interval_mid, interval_end):
    return {
        KEY_TIMEFRAME_AGGREGATION: {
            "filter": {
                "range": {
                    "@timestamp": {
                        "gte": interval_mid.isoformat(),
                        "lte": interval_end.isoformat()
                    },
                },
            },
        },
        KEY_TREND_AGGREGATION: {
            "filter": {
                "range": {
                    "@timestamp": {
                        "gte": interval_start.isoformat(),
                        "lte": interval_mid.isoformat()
                    },
                },
            },
        }
    }


def get_referrer_aggregation(msid=None):
    return {
        "terms": {
            "field": "referrerlabel"
        },
        "aggs": {
            KEY_TIMEFRAME_AGGREGATION: {
                "cardinality": {
                    "field": "fingerprint"
                }
            }
        },
        "meta": {
            KEY_METADATA_FIELD_MSID: msid
        }
    }


def get_devices_aggregation(msid=None):
    return {
        "terms": {
            "field": "deviceclass"
        },
        "aggs": {
            KEY_TIMEFRAME_AGGREGATION: {
                "cardinality": {
                    "field": "fingerprint"
                }
            }
        },
        "meta": {
            KEY_METADATA_FIELD_MSID: msid
        }
    }


def get_interval_filter_exclude_bots(interval_start, interval_end, exists_msid=False, msid=None):
    query = {
        "bool": {
            "filter": [
                {
                    "range": {
                        "@timestamp": {
                            "gte": interval_start.isoformat(),
                            "lte": interval_end.isoformat()
                        }
                    }
                },
                {
                    "match_phrase": {
                        "reloaded": "false"
                    }
                },
                {
                    "match_phrase": {
                        "tazlocal": "false"
                    }
                }
            ],
            "minimum_should_match": 1,
            "should": [
                {
                    "match_phrase": {
                        "DoNotTrack": "\"0\""
                    }
                },
                {
                    "match_phrase": {
                        "DoNotTrack": "\"-\""
                    }
                }
            ],
            "must": [],
            "must_not": [
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
    if msid:
        msid_filter = {
            "match_phrase": {
                "msid": msid
            }
        }
        query['bool']['filter'].append(msid_filter)
    if exists_msid:
        exists_msid = {
                "exists": {
                    "field": "msid"
                }
        }
        query['bool']['must'].append(exists_msid)
    return query


def get_interval_filter_exclude_bots_with_msids(interval_start, interval_end, msids):
    base_query = get_interval_filter_exclude_bots(interval_start, interval_end)

    msid_query = {
        "terms": {
            "msid": msids
        }
    }
    base_query["bool"]["filter"].append(msid_query)
    return base_query


def get_subject_aggregation(limit=10):
    return {
        "terms": {
            "field": "schwerpunkte",
            "order": {
                KEY_FINGERPRINT_AGGREGATION: "desc"
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


def get_hits_interval_msid(min_date, max_date, msid):
    query = {
        "aggs": {
            KEY_TOPLIST_AGGREGATION: {
                "terms": {
                    "field": "msid",
                },
                "aggs": {
                    KEY_TREND_AGGREGATION: {
                        "cardinality": {
                            "field": "fingerprint"
                        }
                    }
                },
                "meta": {
                    KEY_METADATA_FIELD_MSID: msid
                }
            }
        },
        "size": '0',
        "query": get_interval_filter_exclude_bots(min_date, max_date, msid=msid)
    }
    return query
