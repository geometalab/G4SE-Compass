from time import sleep

from django.db import connection, transaction
import pytest
from pathlib import Path, PurePath


def run_sql(path):
    f = open(path, "r")
    sql = f.read()
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.atomic()


@pytest.fixture
def setup_database(db):
    """
    Create custom database fields and populate them with data
    """
    sql = str(PurePath(Path(__file__).parents[3], "setup_database.sql"))
    data = str(PurePath(Path(__file__).parents[1], "testdata.sql"))
    run_sql(sql)
    run_sql(data)
