from tsg import *
from copy import deepcopy
import types

from operator import itemgetter, attrgetter, methodcaller

class S_Type(EnumBase): S_VALUE, S_LIST, S_CHOICE, S_CHOICE_MULTI, S_MULTLINE = range(5)

# Make constants just to make schema look nice
S_VALUE = S_Type.S_VALUE
S_LIST= S_Type.S_LIST
S_CHOICE = S_Type.S_CHOICE
S_CHOICE_MULTI = S_Type.S_CHOICE_MULTI
S_MULTLINE = S_Type.S_MULTLINE

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
    if isinstance(value, str):
        key_value_string += '"' + value + '"'
    elif isinstance(value, bool):
        # JSON boolean uses 'true/false' not 'True/False' as in Python
        if value:
            key_value_string += 'true'
        else:
            key_value_string += 'false'
    else:
        key_value_string += str(value)
    schema_line = makeSchemaLine(indent, key_value_string, line_end)
    return schema_line


