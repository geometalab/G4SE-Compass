from django.db import connection, transaction
import pytest
from pathlib import Path, PurePath
from api.models import Record, HarvestedRecord


def run_sql(path):
    f = open(path, "r")
    sql = f.read()
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.atomic()


@pytest.fixture(scope='session')
def setup_database():
    """
    Create custom database fields and populate them with data
    """
    databasefields = str(PurePath(Path(__file__).parents[3], "database.sql"))
    data = str(PurePath(Path(__file__).parents[1], "testdata.sql"))
    run_sql(databasefields)
    run_sql(data)
