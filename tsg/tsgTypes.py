from tsg import *

class S_Type(EnumBase): S_VALUE, S_LIST, S_CHOICE = range(3)

S_VALUE = S_Type.S_VALUE
S_LIST= S_Type.S_LIST
S_CHOICE = S_Type.S_CHOICE

class T_ATOM(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_ATOM'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_TEXT(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_TEXT'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_BOOLEAN(Symbol):
    def __init__(self, sType=S_CHOICE, *args, **kwargs):
        self.tType = 'T_BOOLEAN'
        self.sType = sType
        super().__init__(self, *args, **kwargs)


class T_IP(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_IP'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_PEM(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_IP'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_CN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_CN'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_CN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_CN'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_CN_PATTERN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_CN_PATTERN'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_UID_PATTERN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_UID_PATTERN'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_EMAIL_PATTERN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_EMAIL_PATTERN'
        self.sType = sType
        super().__init__(self, *args, **kwargs)



class T_IP(Symbol):
    def __init__(self,  sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_IP'
        self.sType = sType
        super().__init__(self, *args, **kwargs)
