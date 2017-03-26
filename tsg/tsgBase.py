from tsg import *

''' Base class for sections and symbols in a schema.

'''
class Base():
    counter = 0;

    def __init__(self, *args, **kwargs):
        self.argument_options = kwargs

        # The Tutus type is the same as the class name.
        self.tType = self.__class__.__name__

        # id_no is used to maintain the order objects are created in.
        Base.counter += 1
        self.id_no = Base.counter

    @classmethod
    def makeArrayFromKeyValue(cls, key, value):
        specLine = ''
        specLine += 'array(' + key + ', '
        if isinstance(value, str):
            specLine += '\'' + value + '\''
        elif isinstance(value, list):
            specLine += Base.makeArrayFromList(value)
        else:
            specLine += str(value)
        specLine += ')'
        return specLine

    @classmethod
    def makeArrayFromList(cls, a_list):
        specLine = ''
        specLine += 'array('
        for value in a_list:
            if isinstance(value, str):
                specLine += '\'' + value + '\''
                # JSON boolean uses 'true/false' not 'True/False' as in Python
                if value:
                    specLine += 'true'
                else:
                    specLine += 'false'
            elif isinstance(value, list):
                specLine += Base.makeArrayFromList(value)
            else:
                specLine += str(value)
            if value != a_list[-1]:
                specLine += ', '
        specLine += ')'
        return specLine
