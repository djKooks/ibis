import os
import ibis
import pytest


CLICKHOUSE_HOST = os.environ.get('IBIS_CLICKHOUSE_HOST', 'localhost')
CLICKHOUSE_PORT = int(os.environ.get('IBIS_CLICKHOUSE_PORT', 9000))
CLICKHOUSE_USER = os.environ.get('IBIS_CLICKHOUSE_USER', 'default')
CLICKHOUSE_PASS = os.environ.get('IBIS_CLICKHOUSE_PASS', '')
IBIS_TEST_CLICKHOUSE_DB = os.environ.get('IBIS_TEST_DATA_DB', 'ibis_testing')


@pytest.fixture(scope='module')
def con():
    return ibis.clickhouse.connect(
        host=CLICKHOUSE_HOST,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASS,
        database=IBIS_TEST_CLICKHOUSE_DB,
    )


@pytest.fixture(scope='module')
def db(con):
    return con.database()


@pytest.fixture(scope='module')
def alltypes(db):
    return db.functional_alltypes


@pytest.fixture(scope='module')
def df(alltypes):
    return alltypes.execute()


@pytest.fixture
def translate():
    from ibis.clickhouse.compiler import ClickhouseExprTranslator
    return lambda expr: ClickhouseExprTranslator(expr).get_result()
