import pytest
from tsg import *


def action(self, data, parent, path):
    print ("---------")
    print("Data=")
    print(data)
    path_string = '/'.join(path)
    print("Path=" + path_string)

T_TEXT.action = action
T_DECIMAL.action = action
Section.action = action

@pytest.fixture
def schema_1():
    class NetworkConfigration(Schema):
        class Sub(Section):
            d = T_DECIMAL()
        t = T_TEXT()
        s = Sub()

    schema = NetworkConfigration()
    return schema

def test_schema_1_1(schema_1):
    conf = {"t": "Kalle", "s": {"d":17}}
    schema_1.parseConf(conf)