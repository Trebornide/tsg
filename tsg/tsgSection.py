from tsg import *

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
