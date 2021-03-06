from tsg import *

class SubConf(Section):
    o1 = OneOf([
        T_IP_ADDRESS(),
        T_DECIMAL()
    ])

class SubConf2(Section):
    class Options():
        description = 'Description of SubConf2'
        title = 'O_SubConf2'
        tralala= 'hoho'

    o2 = OneOf([
        T_IP_ADDRESS(),
        T_DECIMAL()
    ])


class Conf(Schema):
    myAtom = T_ATOM(title='MyTitle', format='T_ATOM', layoutHint=['lowercase', ('vertical', 7), 88])
    sub = OneOf([
        T_DOMAIN_NAME(),
        SubConf(),
        SubConf2(title = 'Kalle', tralala = 'overridden')
    ], description='Why choose?')

conf = Conf()

schema = conf.getSchema()
print (schema)

spec = conf.getSpec()
print (spec)

class Conf1(Schema):
    myInt  = T_DECIMAL(title='My number', minimum=3, maximum=88)
    myString = T_TEXT(title='My string', default='A default')

conf1 = Conf1()
schema = conf1.getSchema()
print(schema)

class Conf2(Schema):
    value = OneOf([
        T_DECIMAL(title='My number', minimum=3, maximum=88),
        T_TEXT(title='My string', default='A default'),
        SubConf(title='Subconf')
    ], title='Please select value type')
    subConf2 = SubConf2(title='Subconf2')

conf2 = Conf2()
schema = conf2.getSchema()
print(schema)