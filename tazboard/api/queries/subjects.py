from django.utils import timezone

from tazboard.api.queries.common import maybe_add_msid_filter, get_interval_filter_exclude_bots, get_subject_aggregation
from tazboard.api.queries.constants import KEY_SUBJECTS_AGGREGATION


def get_subjects_query(min_date, max_date=timezone.now(), limit=10):
    query = {
        "aggs": {
            KEY_SUBJECTS_AGGREGATION: get_subject_aggregation(limit)
        },
        "size": 0,
        "docvalue_fields": [
            {
                "field": "@timestamp",
                "format": "date_time"
            }
        ],
        "query": get_interval_filter_exclude_bots(min_date, max_date)
    }
    return query
