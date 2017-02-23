from tsg import *

class CA(NSection):
    name = T_ATOM()
    cn = T_CN(displayName='CA Common Name')
    pem = T_PEM()

class CAs(Section):
    ca = CA()

class Identity(NSection):
    name = T_ATOM()
    cn = T_CN_PATTERN('S_LIST', max=32, optional=True)
    uid = T_UID_PATTERN('S_LIST', max=32, optional=True)
    email = T_EMAIL_PATTERN('S_LIST', max=32, optional=True)

class Identities(Section):
    identities = Identity(max = 1024)

class Networks(NSection):
    enable = T_BOOLEAN()
    name = T_TEXT()
    address = T_IP(mask=True)
    gateway = T_IP()

class DHCP(Section):
    enable = T_BOOLEAN()
    dns = T_BOOLEAN()
    defaultRouter = T_BOOLEAN()

class RoutedInterface(Section):
    enable = T_BOOLEAN()
    name = T_TEXT()
    address = T_IP()
    networks = Networks()
    dhcp = DHCP()

class Device(NSection):
    name = T_ATOM()
    enable = T_BOOLEAN()
    deviceType = T_TEXT('S_CHOICE', choices = ['KryApp 9411 - M100', 'KryApp 9411 - C200', 'KryApp 9411 - R200', 'KryApp 9411 - R210', 'KryApp 9411 - H200', 'KryApp 9411 - H210', 'KryApp 9411 - H300'])
    mgmt1 = RoutedInterface()
    mgmt2 = RoutedInterface()

class Devices(Section):
    device = Device()

class Configuration(Section):
    ca = CAs(displayName='CA')
    identities = Identities()
    device = Devices()

conf = Configuration()
spec = conf.getSpec()

print(spec)
