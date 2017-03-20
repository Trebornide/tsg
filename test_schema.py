from tsg import *
from test import NetworkConfigration


class SubConf(Section):
    o1 = OneOf([
        T_IP(),
        T_DECIMAL()
    ])

class SubConf2(Section):
    class Options():
        description = 'Description of SubConf2'

    o2 = OneOf([
        T_IP(),
        T_DECIMAL()
    ])


class Conf(Configuration):
    myAtom = T_ATOM(title='MyTitle', format='T_ATOM', layoutHint=('lowercase', ('vertical', 7)))
    sub = OneOf([
        T_DOMAIN_NAME(),
        SubConf(),
        SubConf2(title = 'Kalle')
    ], description='Why choose?')

#conf = NetworkConfigration()
conf = Conf()

schema = conf.getSchema()
print (schema)

spec = conf.getSpec()
print (spec)
