from tsg import *


class T_ATOM(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_ATOM'
        self.sType = sType
        self.type = 'string'
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

class T_DECIMAL(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_DECIMAL'
        self.sType = sType
        super().__init__(self, *args, **kwargs)


class T_IP(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_IP'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_IP_REDUCED(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_IP_REDUCED'
        self.sType = sType
        super().__init__(self, *args, **kwargs)

class T_PORT(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_PORT'
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

class T_DOMAIN_NAME(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_DOMAIN_NAME'
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

class T_SECTION(Symbol):
    def __init__(self, sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_SECTION'
        self.sType = sType
        super().__init__(self, *args, **kwargs)



class T_IP(Symbol):
    def __init__(self,  sType=S_VALUE, *args, **kwargs):
        self.tType = 'T_IP'
        self.sType = sType
        super().__init__(self, *args, **kwargs)
