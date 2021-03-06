from tsg import *

class Symbol(Base):

    def __init__(self, *args, **kwargs):
       super().__init__(self, *args, **kwargs)


    def getSpec(self, path=[]):
        specLine = ' symbol('

        for p in path:
            specLine += '\'' + p + '\''
            specLine += ', '

        # E.g. S_VALUE
        specLine += S_Type.tostring(self.sType) + ', '
        # E.g. T_TEXT
        specLine += self.tType + ', '

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
        schema += makeKeyValueSchemaLine(indent, 's_type', S_Type.tostring(self.sType))

        # Options
        if self.argument_options != None:
            for key, value in self.argument_options.items():
                schema += makeKeyValueSchemaLine(indent, key, value)
        schema = schema.rstrip(',\n')
        schema += '\n'

        return schema


    def parseConf(self, conf, parent, path):
        self.parent = parent
        self.path = path

        if type(conf) == 'str':
            assert 'string' == self.type
        try:
            self.action(conf, self.parent, self.path)
        except AttributeError:
            pass

