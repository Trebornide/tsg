import pytest
from tsg import *

@pytest.fixture
def schema_1():
    class NetworkConfigration(Schema):
        t = T_TEXT()

    schema = NetworkConfigration()
    return schema

def test_1():
    assert 1 == 1

def test_schema_1_1(schema_1):
    conf = {"t": "Kalle"}
    schema_1.parseConf(conf)