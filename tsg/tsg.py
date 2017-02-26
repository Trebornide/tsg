from copy import deepcopy
from tsg import *
from operator import itemgetter, attrgetter, methodcaller

def makeSchemaLine(indent, line):
    schemaLine = ''
    for i in range(1, indent):
        schemaLine += ' '
    schemaLine += line
    schemaLine += '\n'
    return schemaLine


class Base():
    counter = 0;


    def __init__(self, *args, displayName=None,**kwargs):
        self.displayName = displayName
        self.kwargs = kwargs
        Base.counter += 1
        self.idNo = Base.counter

    @classmethod
    def makeArrayFromKeyValue(cls, key, value):
        specLine = ''
        specLine += 'array(' + key + ', '
        if type(value) is str:
            specLine += '\'' + value + '\''
        elif type(value) is list:
            specLine += Base.makeArrayFromList(value)
        else:
            specLine += str(value)
        specLine += ')'
        return specLine

    @classmethod
    def makeArrayFromList(cls, list):
        specLine = ''
        specLine += 'array('
        for value in list:
            if type(value) is str:
                specLine += '\'' + value + '\''
            elif type(value) is list:
                specLine += Base.makeArrayFromList(value)
            else:
                specLine += str(value)
            if value != list[-1]:
                specLine += ', '
        specLine += ')'
        return specLine

class Symbol(Base):

    def __init__(self, *args, **kwargs):
       super().__init__(self, *args, **kwargs)


    def getSpec(self, path=[]):
        specLine = 'symbol('

        for p in path:
            specLine += '\'' + p + '\''
            specLine += ', '

        specLine += self.tType + ', '
        specLine += S_Type.tostring(self.sType) + ', '

        if self.kwargs != None:
            for key, value in self.kwargs.items():
                specLine += Base.makeArrayFromKeyValue(key, value)
                specLine += ', '

        specLine = specLine.strip(', ')
        specLine += ');\n'
        return specLine

class Section(Base):

    def getOwnSpec(self, path=[]):
        specLine = 'section('
        for p in path:
            specLine += '\'' + p + '\''
            specLine += ', '

        if isinstance(self, NSection):
            specLine += 'N_SECTION_NUMBERED' + ', '

        if self.kwargs != None:
            for key, value in self.kwargs.items():
                specLine += Base.makeArrayFromKeyValue(key, value)
                specLine += ', '

        specLine = specLine.strip(', ')
        specLine += ');\n'
        return specLine

    def getSpec(self, path = []):
        spec = ''

        # Comment spec file using class doc
        if self.__doc__ != None:
            for docLine in self.__doc__.split('\n'):
                spec += '# ' + docLine.strip() + '\n'

        spec += self.getOwnSpec(path)

        items = self.__class__.__dict__.items()

        # Find attributes with base class Base() and
        # sort them in the order they where created.
        attrList = []
        for k1, v1 in items:
            if isinstance(v1, Base):

                # All atributes with base class Base has a running number
                # telling the order they where created.
                attrList.append((v1.idNo, k1, v1))

        # Sort attributes in the same order as they where created
        sortedAttrList = sorted(attrList)

        # Iterate over sections attributes and recurse into sub-nodes.
        for dummy, k1, v1 in sortedAttrList:
            nextLevelPath = deepcopy(path)
            nextLevelPath.append(k1)
            spec += v1.getSpec(nextLevelPath)
        return spec

    def getSchema(self, indent=0):
        pass

class NSection(Section):
    pass

class Configuration(Section):
    def getSchema(self, indent=0):
        schema = makeSchemaLine(indent, '{')
        indent += 4
        schema += makeSchemaLine(indent, '"$schema": "http://json-schema.org/draft-04/schema#"')
        # TODO: Definitions
        indent -= 4

        schema += makeSchemaLine(indent, '}')
        return schema


