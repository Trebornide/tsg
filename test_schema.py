from tsg import *
from test import Conf

class SubConf(Section):
    s1 = T_ATOM()

#class Conf(Configuration):
#    myAtom = T_ATOM(title='MyTitle', format='T_ATOM', layoutHint=('lowercase', ('vertical', 7)))
#    sub = SubConf()

conf = Conf()

schema = conf.getSchema()
print (schema)

