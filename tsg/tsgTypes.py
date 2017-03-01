from tsg import *


class T_ATOM(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_TEXT(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_BOOLEAN(Symbol):
    def __init__(self, sType=S_CHOICE, *args, **kwargs):
        self.type = 'boolean'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_DECIMAL(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'number'
        self.sType = sType
        super().__init__(self, *args, **kwargs)


class T_IP(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_IP_REDUCED(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_PORT(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'number'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_PEM(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_CN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_CN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_CN_PATTERN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_DOMAIN_NAME(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_UID_PATTERN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_EMAIL_PATTERN(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_SECTION(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.type = 'object'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_IP(Symbol):
    def __init__(self,  sType=S_VALUE, *args, **kwargs):
        self.type = 'string'
        self.sType = sType
        super().__init__(self, *args, **kwargs)
