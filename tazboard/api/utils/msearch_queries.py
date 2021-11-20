from rest_framework.utils import json


def prepare_msearch_query(query, query_indices=None):
    if query_indices is None:
        query_indices = []

    if isinstance(query, list):
        queries = query
    else:
        queries = [query]

    # create a multi-search body
    body = ""
    for i, q in enumerate(queries):
        # check if there is a definition for an index to use
        # otherwise use default index
        if i < len(query_indices):
            body += json.dumps({"index": query_indices[i]}) + "\n"
        else:
            body += json.dumps({}) + "\n"
        # ndjson lines; last line must be terminated with a newline
        body += json.dumps(q) + "\n"

    return body
