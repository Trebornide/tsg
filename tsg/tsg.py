from copy import deepcopy
from operator import itemgetter, attrgetter, methodcaller

class Base():
    counter = 0;

    def __init__(self, *args, **kwargs):
        #        self.displayName = displayName
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
        # self.tType = tType
        # self.sType = sType
        super().__init__(self, *args, **kwargs)

    #


    def getSpec(self, path=[]):
        specLine = 'symbol('

        for p in path:
            specLine += '\'' + p + '\''
            specLine += ', '

        specLine += self.tType + ', '
        specLine += self.sType + ', '

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

        spec = self.getOwnSpec(path)

        items = self.__class__.__dict__.items()

        # Find attributes with base class Base() and
        # sort them in the order they where created.
        attrList = []
        for k1, v1 in items:
            if isinstance(v1, Base):
                attrList.append((v1.idNo, k1, v1))
        sortedAttrList = sorted(attrList)

        # Iterate over sections attributes and recurse into sub-nodes.
        for dummy, k1, v1 in sortedAttrList:
            if isinstance(v1, Base):
                nextLevelPath = deepcopy(path)
                nextLevelPath.append(k1)
                spec += v1.getSpec(nextLevelPath)
        return spec

class NSection(Section):
    pass

class Configuration(Section):
    pass
