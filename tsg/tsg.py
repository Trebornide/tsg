from tsg import *
from copy import deepcopy

from operator import itemgetter, attrgetter, methodcaller

class S_Type(EnumBase): S_VALUE, S_LIST, S_CHOICE, S_CHOICE_MULTI = range(4)

# Make constants just to make schema look nice
S_VALUE = S_Type.S_VALUE
S_LIST= S_Type.S_LIST
S_CHOICE = S_Type.S_CHOICE
S_CHOICE_MULTI = S_Type.S_CHOICE_MULTI

def makeSchemaLine(indent, line, line_end=',\n'):
    schema_line = ''
    for i in range(1, indent):
        schema_line += ' '
    schema_line += line
    schema_line += line_end
    return schema_line

def makeKeyValueSchemaLine(indent, key, value, line_end=',\n'):
    key_value_string = ''
    key_value_string += '"' + key + '": '
    if type(value) is str:
        key_value_string += '"' + value + '"'
    else:
        key_value_string += str(value)
    schema_line = makeSchemaLine(indent, key_value_string, line_end)
    return schema_line


class Base():
    counter = 0;


    def __init__(self, *args, displayName=None,**kwargs):
        self.displayName = displayName
        self.argument_options = kwargs
        self.tType = self.__class__.__name__

        # id_no is used to maintain the order objects are created in.
        Base.counter += 1
        self.id_no = Base.counter

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
        specLine = ' symbol('

        for p in path:
            specLine += '\'' + p + '\''
            specLine += ', '

        specLine += self.tType + ', '
        specLine += S_Type.tostring(self.sType) + ', '

        if self.argument_options != None:
            for key, value in self.argument_options.items():
                specLine += Base.makeArrayFromKeyValue(key, value)
                specLine += ', '

        specLine = specLine.rstrip(', ')
        specLine += ');\n'
        return specLine

    def getSchema(self, indent):
        schema = ''
        schema += makeKeyValueSchemaLine(indent, 'type', self.type )
        schema += makeKeyValueSchemaLine(indent, 't_type', self.tType)

        # Options
        if self.argument_options != None:
            for key, value in self.argument_options.items():
                schema += makeKeyValueSchemaLine(indent, key, value)
        schema = schema.rstrip(',\n')
        schema += '\n'

        return schema


class Section(Base):

    def getOptions(self):
        options = {}

        try:
            class_options = self.Options.__dict__.items()
            for key, value in class_options:
                if not key.startswith('__'):
                    options[key] = value
            pass
        except:
            pass

        # Options
        if self.argument_options != None:
            for key, value in self.argument_options.items():
                options[key] = value

        return options

    def getOwnSpec(self, path=[]):
        specLine = 'section('
        for p in path:
            specLine += '\'' + p + '\''
            specLine += ', '

        if isinstance(self, NSection):
            specLine += 'N_SECTION_NUMBERED' + ', '
        elif isinstance(self, OneOf):
            specLine += 'ONEOF_SECTION' + ', '

        options = self.getOptions()

        for key, value in options.items():
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
                attrList.append((v1.id_no, k1, v1))

        # Sort attributes in the same order as they where created
        sortedAttrList = sorted(attrList)

        # Iterate over sections attributes and recurse into sub-nodes.
        for dummy, k1, v1 in sortedAttrList:
            nextLevelPath = deepcopy(path)
            nextLevelPath.append(k1)
            spec += v1.getSpec(nextLevelPath)
        return spec

    def getSchema(self, indent=0):
        schema = ''
        schema += makeKeyValueSchemaLine(indent, 'type', 'object')
        schema += makeKeyValueSchemaLine(indent, 'additionalProperties', False)

        options = self.getOptions()

        # Options
        for key, value in options.items():
            schema += makeKeyValueSchemaLine(indent, key, value)
        schema = schema.rstrip(',\n')
        schema += '\n'

        items = self.__class__.__dict__.items()

        # Find attributes with base class Base() and
        # sort them in the order they where created.
        attrList = []
        for k1, v1 in items:
            if isinstance(v1, Base):
                # All atributes with base class Base has a running number
                # telling the order they where created.
                attrList.append((v1.id_no, k1, v1))

        # Sort attributes in the same order as they where created
        sortedAttrList = sorted(attrList)

        schema += makeSchemaLine(indent, '"properties": {', '\n')
        indent += 4

        # Iterate over properties and recurse into sub-nodes.
        for dummy, k1, v1 in sortedAttrList:
            schema += makeSchemaLine(indent, '"' + k1 + '": {', '\n')
            schema += v1.getSchema(indent + 4)
            schema += makeSchemaLine(indent, '}')

        # Remove ',' from last attribute in tuple
        schema = schema.rstrip(',\n')
        schema += '\n'

        # End of properties block
        indent -= 4
        schema += makeSchemaLine(indent, '}', '\n')

        return schema

class NSection(Section):
    pass

class OneOf(Section):
    def __init__(self, one_of_list, *args, **kwargs):
        self.oneOf = one_of_list
        super().__init__(self, *args, **kwargs)


    def getSpec(self, path=[]):
        spec = ''

        # Comment spec file using class doc
        if self.__doc__ != None:
            for docLine in self.__doc__.split('\n'):
                spec += '# ' + docLine.strip() + '\n'

        spec += self.getOwnSpec(path)

        # Iterate over sections attributes and recurse into sub-nodes.
        for v1 in self.oneOf:
            spec += v1.getSpec(path)
        return spec


    def getSchema(self, indent=0):
        schema = ''

        # Options
        if self.argument_options != None:
            for key, value in self.argument_options.items():
                schema += makeKeyValueSchemaLine(indent, key, value)

        schema += makeSchemaLine(indent, '"oneOf": [', '\n')
        indent += 4

        # Iterate over the possible sub-schemas.
        for v1 in self.oneOf:
            schema += makeSchemaLine(indent, '{', '\n')
            schema += v1.getSchema(indent + 4)
            schema += makeSchemaLine(indent, '}')

        # Remove ',' from last attribute in list
        schema = schema.rstrip(',\n')
        schema += '\n'

        # End of oneOf list
        indent -= 4
        schema += makeSchemaLine(indent, ']', '\n')

        return schema


class AnyOfSection(Section):
    pass

class Configuration(Section):
    def getSchema(self, indent=0):
        schema = makeSchemaLine(indent, '{', '\n')
        indent += 4
        schema += makeSchemaLine(indent, '"$schema": "http://tutus.se/draft-01/farist-config-schema#"')
        schema += super().getSchema(indent)
        indent -= 4

        schema += makeSchemaLine(indent, '}', '')
        return schema


