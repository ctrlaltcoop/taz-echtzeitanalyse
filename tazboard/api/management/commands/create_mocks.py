import json

from django.core.management import BaseCommand

from tazboard.api.elastic_client import es
from tazboard.api.queries.histogram import get_histogram_query
from tazboard.api.queries.referrer import get_referrer_query
from tazboard.api.queries.toplist import get_toplist_query
from tazboard.api.tests.common import get_mock_filepath_for_query


def get_argument_matrix(list_a, list_b):
    for i in list_a:
        for j in list_b:
            yield i + j


class Command(BaseCommand):
    query_configs = [
        {
            'get_query': get_histogram_query,
            'arguments': [
                ('now-24h', 'now'),
            ]
        },
        {
            'get_query': get_referrer_query,
            'arguments': [
                ('now-10m', 'now'),
                ('now-24h', 'now'),
                ('now-1w', 'now'),
                ('now-1M', 'now')
            ]
        },
        {
            'get_query': get_toplist_query,
            'arguments': get_argument_matrix((
                ('now-10m', 'now'),
                ('now-24h', 'now'),
                ('now-1w', 'now'),
                ('now-1M', 'now'),
            ), (('10',), ('25',)))
        }
    ]

    def handle(self, *args, **options):
        for config in self.query_configs:
            for arguments in config['arguments']:
                query_fn = config['get_query']
                query = query_fn(*arguments)
                with open(get_mock_filepath_for_query(query), 'w') as outfile:
                    response = es.search(body=query)
                    outfile.write(json.dumps(response, indent=4))

