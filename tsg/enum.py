class EnumBase: # base class of all Enums
    @classmethod
    def tostring(cls, value):
        dict = cls.__dict__
        for k, v in dict.items():
            if v == value:
                return str(k)

    @classmethod
    def fromstring(cls, name):
        return cls.__dict__[name]

#class S_Type(EnumBase): S_VALUE, S_LIST, S_CHOICE = range(3)
