from django.db import connection, transaction
import pytest
from pathlib import Path, PurePath
from django.contrib.auth.models import User


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
    sql = str(PurePath(Path(__file__).parents[3], "setup_database.sql"))
    data = str(PurePath(Path(__file__).parents[1], "testdata.sql"))
    run_sql(sql)
    run_sql(data)


@pytest.fixture(scope='class')
def test_user():
    User.objects.create_superuser('admin', 'admin@test.com', 'securepassword')
