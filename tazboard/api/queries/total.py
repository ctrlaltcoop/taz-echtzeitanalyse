from django.utils import timezone

from tazboard.api.queries.common import get_interval_filter_exclude_bots, get_ranges, maybe_add_msid_filter


def get_total_query(min_date, max_date=timezone.now(), msid=None):
    min_date_previous_interval = min_date - (max_date - min_date)
    query = {
        "aggs": {
            **get_ranges(
                min_date_previous_interval, min_date, max_date
            ),
        },
        "query": get_interval_filter_exclude_bots(min_date_previous_interval, max_date)
    }
    query = maybe_add_msid_filter(msid, query)
    return query
