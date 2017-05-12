from tsg import *
import datetime

class Schema(Section):
    def getSchema(self, indent=0):
        schema = makeSchemaLine(indent, '{', '\n')
        indent += 4
        schema += makeSchemaLine(indent, '"$schema": "http://tutus.se/draft-01/farist-config-schema#"')
        schema += super().getSchema(indent)
        indent -= 4

        schema += makeSchemaLine(indent, '}', '')
        return schema


    def getSpec(self, major, minor, path = []):
        spec = ''

        # Comment spec file using class doc
        if self.__doc__ != None:
            for docLine in self.__doc__.split('\n'):
                spec += '// ' + docLine.strip() + '\n'

        spec += '<?\n'
        spec += 'version(\'farist-vpn-net\', ' + str(major) + ', ' + str(minor) + ');\n\n'

        time_list = []
        time_list.append(datetime.datetime.today())
        spec += '//  Generated at: ' + str(time_list[0]) + '\n\n'

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

        spec += '\n?>\n'

        return spec
