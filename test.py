from tsg import *

time_zones = ['Africa/Casablanca', 'Africa/Dakar', 'Africa/Johannesburg', 'Africa/Khartoum',
              'Africa/Luanda', 'Africa/Maputo', 'Africa/Nairobi', 'Africa/Tunis', 'America/Anchorage',
              'America/Argentina/Buenos_Aires', 'America/Bogota', 'America/Caracas', 'America/Chicago',
              'America/Halifax', 'America/Los_Angeles', 'America/Mexico_City', 'America/New_York',
              'America/Phoenix', 'America/Puerto_Rico', 'America/Santiago', 'America/Sao_Paulo',
              'America/St_Johns', 'America/Tijuana', 'America/Toronto', 'America/Vancouver',
              'America/Winnipeg', 'Asia/Almaty', 'Asia/Baghdad', 'Asia/Baku', 'Asia/Bangkok',
              'Asia/Colombo', 'Asia/Dhaka', 'Asia/Dubai', 'Asia/Ho_Chi_Minh', 'Asia/Irkutsk',
              'Asia/Jakarta', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Karachi', 'Asia/Kathmandu',
              'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Manila', 'Asia/Novosibirsk', 'Asia/Pyongyang',
              'Asia/Riyadh', 'Asia/Seoul', 'Asia/Singapore', 'Asia/Tashkent', 'Asia/Tehran', 'Asia/Tokyo',
              'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yekaterinburg', 'Atlantic/Azores', 'Atlantic/Cape_Verde',
              'Atlantic/South_Georgia', 'Australia/Adelaide', 'Australia/Perth', 'Australia/Sydney',
              'Europe/Belgrade', 'Europe/Berlin', 'Europe/Brussels', 'Europe/Helsinki', 'Europe/Istanbul',
              'Europe/Kiev', 'Europe/Lisbon', 'Europe/London', 'Europe/Madrid', 'Europe/Paris', 'Europe/Rome',
              'Europe/Stockholm', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Honolulu', 'Pacific/Nauru',
              'Pacific/Niue', 'Pacific/Port_Moresby']
class CAs(Section):
    '''
    CA used by device.
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

class CommonConfigs(Section):
    '''
    CommonConfigs used by device.
    '''

    class CommonConfig(NSection):
        class CAdmin(Section):
            enable    = T_BOOLEAN()
            port      = T_PORT(default=443)
            administrators = T_SECTION(S_CHOICE, choices='sections', sections=[':identity:identity'])
            operators = T_SECTION(S_CHOICE, choices='sections', sections=[':identity:identity'])

        class Certificates(Section):
            allowedCA = T_SECTION(S_CHOICE_MULTI, max=32, choices='section', section=[':certificate:ca'])
            allowExpiredCert = T_BOOLEAN()

        class Syslog(Section):
            enabled = T_BOOLEAN(default=False)
            server = T_IP_REDUCED(S_LIST)

        class General(Section):
            timeZone = T_ATOM(S_CHOICE, choices=time_zones)

        class NTP(Section):
            '''
            Network Time Protocol
            '''
            class Key(NSection):
                name = T_TEXT()
                number = T_DECIMAL()
                key = T_ATOM()

            class Server(NSection):
                name = T_TEXT()
                server = T_IP_REDUCED()
                key = T_SECTION(S_CHOICE, choices='section', section=[':common:config:ntp:key'])

            key = Key(max=3)
            server = Server(max=3)

        name    = T_ATOM()
        cn      = T_CN(displayName='CA Common Name')
        pem     = T_PEM()
        cadmin  = CAdmin(displayNamez='CAdmin client settings')
        cert    = Certificates()
        syslog  = Syslog()
        general = General()
        ntp     = NTP()

    common = CommonConfig()


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
    address  = T_IP(mask=True)
    networks = Networks()
    dhcp = DHCP()

class LinkInterface(Section):
    enable   = T_BOOLEAN()
    name     = T_TEXT()

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

    class CAdminClientSettings:
        address = T_IP_REDUCED(S_LIST, max=2)
        port = T_PORT(default=443)
        cn = T_CN()
        pollInterval = T_DECIMAL(default=10)

    class Device(NSection):
        name = T_ATOM()
        enable = T_BOOLEAN()
        deviceType = T_TEXT(S_CHOICE, choices=['KryApp 9411 - M100', 'KryApp 9411 - C200', 'KryApp 9411 - R200',
                                               'KryApp 9411 - R210', 'KryApp 9411 - H200', 'KryApp 9411 - H210',
                                               'KryApp 9411 - H300'])
        version = T_TEXT(S_CHOICE, choices=['4.0.5', '4.1', '4.2'], default='4.1')
        hostname = T_DOMAIN_NAME(optional=True)
        failover = T_BOOLEAN(default=False)
        common = T_SECTION(S_CHOICE, choices='section', section=[':common:config'] )
        mgmt1 = RoutedInterface(enableIf=('failover', '==', True))
        mgmt2 = RoutedInterface()
        portpair = PortPairs()

    device = Device()

class Conf(Configuration):
    ca = CAs(displayName='CA')
    identity = Identities()
    common = CommonConfigs()
    device = Devices()

conf = Conf()

spec = conf.getSpec()
print(spec)
