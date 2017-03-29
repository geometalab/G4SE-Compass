import os

os.environ['SECRET_KEY'] = 'secret-testing-key'
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'postgres://postgres:postgres@localhost:5432/G4SE'

from G4SE.settings import *  # noqa

INTERNAL_IP_RANGES = ["127.0.0.1", '172.0.0.0/8']
HAYSTACK_CONNECTIONS['default']['INDEX_NAME'] = 'test_haystack'  # noqa: F405 'HAYSTACK_CONNECTIONS' may be undefined
HAYSTACK_CONNECTIONS['en']['INDEX_NAME'] = 'test_haystack_english'  # noqa: F405
HAYSTACK_CONNECTIONS['de']['INDEX_NAME'] = 'test_haystack_german'  # noqa: F405
HAYSTACK_CONNECTIONS['fr']['INDEX_NAME'] = 'test_haystack_french'  # noqa: F405
