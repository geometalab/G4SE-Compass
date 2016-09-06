import os

os.environ['SECRET_KEY'] = 'secret-testing-key'
os.environ['DATABASE_URL'] = 'postgres://postgres:postgres@localhost:5432/G4SE'

from G4SE.settings import *  # noqa

INTERNAL_IP_RANGES = ["127.0.0.1", '172.0.0.0/8']
