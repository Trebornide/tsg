from tsg import *

class CAs(Section):
    '''
    CA used by device.
    CA doc Line 2
    '''
    class CA(NSection):
        name = T_ATOM()
        cn   = T_CN(displayName='CA Common Name')
        pem  = T_PEM()

    ca = CA()

class Identities(Section):
    '''
    Administrative identities to manage the devices
    '''
    class Identity(NSection):
        name  = T_ATOM(displayName='Admin group name', xxx='yyy')
        cn    = T_CN_PATTERN(S_LIST, max=32, optional=True)
        uid   = T_UID_PATTERN(S_LIST, max=32, optional=True)
        email = T_EMAIL_PATTERN(S_LIST, max=32, optional=True)

    identities = Identity(max = 1024)

class Networks(NSection):
    enable  = T_BOOLEAN()
    name    = T_TEXT()
    address = T_IP(mask=True)
    gateway = T_IP()

class DHCP(Section):
    enable        = T_BOOLEAN()
    dns           = T_BOOLEAN()
    defaultRouter = T_BOOLEAN()

class RoutedInterface(Section):
    enable   = T_BOOLEAN()
    name     = T_TEXT()
    address  = T_IP()
    networks = Networks()
    dhcp = DHCP()


class PortPairs(Section):
    class PortPair(NSection):
        '''Crypto function'''
        enable = T_BOOLEAN()
        name = T_TEXT()
        clear = RoutedInterface()
        crypto = RoutedInterface()
    portpair = PortPair()


class Devices(Section):
    '''
    Färist VPN-devices
    '''
    class Device(NSection):
        name = T_ATOM()
        enable = T_BOOLEAN()
        deviceType = T_TEXT(S_CHOICE, choices=['KryApp 9411 - M100', 'KryApp 9411 - C200', 'KryApp 9411 - R200',
                                               'KryApp 9411 - R210', 'KryApp 9411 - H200', 'KryApp 9411 - H210',
                                               'KryApp 9411 - H300'])
        version = T_TEXT(S_CHOICE, choices=['4.0.5', '4.1', '4.2'], default='4.1')
        failover = T_BOOLEAN(default=False)

        mgmt1 = RoutedInterface(enableIf=('failover', '==', True))
        mgmt2 = RoutedInterface()
        portpair = PortPairs()

    device = Device()

class Conf(Configuration):
    ca = CAs(displayName='CA')
    identity = Identities()
    device = Devices()

conf = Conf()

spec = conf.getSpec()
print(spec)

schema = conf.getSchema()
print (schema)