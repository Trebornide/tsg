from tsg import *

class Conf(Configuration):
    myAtom = T_ATOM(a='b')

conf = Conf()

schema = conf.getSchema()
print (schema)

