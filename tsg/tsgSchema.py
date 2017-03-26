from tsg import *

class Schema(Section):
    def getSchema(self, indent=0):
        schema = makeSchemaLine(indent, '{', '\n')
        indent += 4
        schema += makeSchemaLine(indent, '"$schema": "http://tutus.se/draft-01/farist-config-schema#"')
        schema += super().getSchema(indent)
        indent -= 4

        schema += makeSchemaLine(indent, '}', '')
        return schema


