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

farist4_models = ['KryApp 9411 - M100',
                  'KryApp 9411 - C200',
                  'KryApp 9411 - R200',
                  'KryApp 9411 - R210',
                  'KryApp 9411 - H200',
                  'KryApp 9411 - H210',
                  'KryApp 9411 - H300'
                  ]

portpair = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '2.1', '2.2', '2.3', '2.4']
portpair_extended = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '2.1', '2.2', '2.3', '2.4', 'MacSecAll']

class CAs(Section):
    '''
    CA used by device.
    '''
    class CA(NSection):
        Name = T_ATOM(display='Name')
        CN   = T_CN(display='CA Common Name')
        Location = T_ATOM(S_CHOICE , choices=['Config', 'File', 'Card'])
        PEM  = T_PEM(display='PEM file', conditions=['Location=Config'])
        CRL = T_URL(optional=True)

    ca = CA()

class Identities(Section):
    '''
    Administrative identities to manage the devices 
    '''
    class Options():
        display='Administrators'

    class Identity(NSection):
        Name  = T_ATOM(title='Admin group name')
        CN    = T_CN_PATTERN(S_LIST, max=32, optional=True)
        UID   = T_UID_PATTERN(S_LIST, max=32, optional=True)
        Email = T_EMAIL_PATTERN(S_LIST, max=32, optional=True)

    identity = Identity(max = 1024)

class CommonConfigs(Section):
    '''
    CommonConfigs used by device.
    '''
    class Options():
        display='Common configutations'

    class CommonConfig(NSection):
        class CAdmin(Section):
            Enable        = T_BOOLEAN(default=True)
            Port          = T_PORT(default=443, optional=True)
            Administrator = T_SECTION(S_CHOICE, choices='sections', sections=[':identity:identity'])
            operator      = T_SECTION(S_CHOICE, choices='sections', sections=[':identity:identity'], optional=True)

        class Certificates(Section):
            AllowedCA = T_SECTION(S_CHOICE_MULTI, max=32, choices='section', section=[':certificate:ca'])
            AllowExpiredCert = T_BOOLEAN(default=False)

        class Syslog(Section):
            class Remote(NSection):
                Enable = T_BOOLEAN()
                Host = T_DOMAIN_NAME()
                Protocol = T_ATOM(S_CHOICE, choices=['TCP', 'UDP'], default='TCP')
                Level = T_ATOM(S_CHOICE, choices=['Debug', 'Info', 'Warning', 'Error'], default='Info')

            Storage = T_ATOM(S_CHOICE, choices=['Transient', 'Permanent'], default='Transient')
            History = T_DECIMAL(min=1, max=365, default=90)
            Remote = Remote(max=5)

        class SyslogOld:
            Enable = T_BOOLEAN(default=False)
            Server = T_IP_REDUCED(S_LIST, max=5)

        class General(Section):
            TimeZone = T_ATOM(S_CHOICE, choices=time_zones)

        class NTP(Section):
            '''
            Network Time Protocol
            '''
            class Key(NSection):
                Name = T_TEXT()
                Number = T_DECIMAL()
                Key = T_ATOM()

            class Server(NSection):
                Name = T_TEXT()
                Server = T_IP_REDUCED()
                Key = T_SECTION(S_CHOICE, choices='section', section=[':common:config:ntp:key'])

            Enable = T_BOOLEAN(default=False)
            Key = Key(max=5)
            Server = Server(max=5)

        Name    = T_ATOM()
        cadmin  = CAdmin(display='CAdmin client settings')
        cert    = Certificates(display='CA certificates')
        #syslog  = SyslogOld()
        syslog  = Syslog()
        general = General()
        ntp     = NTP()

    config = CommonConfig()


class CAdminClientSettings(Section):
    CN = T_CN()
    Address = T_IP_REDUCED(S_LIST, max=2)
    PollInterval = T_DECIMAL(default=10)
    Port = T_PORT(default=443)

class Networks(NSection):
    Enable  = T_BOOLEAN(default=True)
    Name    = T_TEXT(optional=True)
    Address = T_IP_ADDRESS(mask=True)
    Gateway = T_IP_ADDRESS(optional=False)

class DHCP(Section):
    Enable        = T_BOOLEAN(default=False)
    DNS           = T_BOOLEAN(default=False)
    DefaultRouter = T_BOOLEAN(default=False)

class ManagementInterface(Section):
    Enable   = T_BOOLEAN(default=True)
    Name     = T_TEXT(optional=True)
    Address  = T_IP_ADDRESS(mask=True)
    Networks = Networks()
    DHCP = DHCP(optional=True)
    MTU      = T_DECIMAL(optional=True)

class RoutedInterface(Section):
    Address  = T_IP_ADDRESS(mask=True)
    MTU      = T_DECIMAL(optional=True)
    Networks = Networks()
    DHCP     = DHCP(optional=True)

class LinkInterface(Section):
    MTU      = T_DECIMAL(optional=True)

class Filters(Section):
    class Filter(NSection):
        # ToDo: OneOf filter type in the future
        Enable = T_BOOLEAN()
        FilterType = T_TEXT(S_CHOICE, choices=['NTP'], default='NTP')
        ClearNTP = T_IP_REDUCED()
        CryptoNTP = T_IP_REDUCED()
    Filter = Filter()

class RoutedPortPairs(NSection):
    class RoutedPortPair(Section):
        '''Crypto function'''
        Enable = T_BOOLEAN()
        Name = T_TEXT()
        PortPair = T_TEXT(S_CHOICE, choices=portpair)
        clear = RoutedInterface()
        crypto = RoutedInterface()
        filter = Filters()

    portpair = RoutedPortPair()

class BridgedPortPairs(NSection):
    class BridgedPortPair(Section):
        '''Crypto function'''
        Enable = T_BOOLEAN()
        Name = T_TEXT()
        PortPair = T_TEXT(S_CHOICE, choices=portpair)
        clear = LinkInterface()
        crypto = RoutedInterface()
    portpair = BridgedPortPair()

class LinkedPortPairs(NSection):
    class LinkedPortPair(Section):
        '''Crypto function'''
        Enable = T_BOOLEAN()
        Name = T_TEXT()
        PortPair = T_TEXT(S_CHOICE, choices=portpair)
        MTU      = T_DECIMAL(optional=True)
    portpair = LinkedPortPair()

class Interface(Section):
    mgmt1 = ManagementInterface()
    mgmt2 = ManagementInterface()

class Devices(Section):
    '''
    Färist VPN-devices
    '''
    class Options():
        display='VPN devices'

    class Device(NSection):
        Name = T_ATOM()
        Enable = T_BOOLEAN()
        DeviceType = T_TEXT(S_CHOICE, choices=farist4_models)
        Version = T_TEXT(S_CHOICE, choices=['4.0.5', '4.1', '4.2'], default='4.1')
        Hostname = T_DOMAIN_NAME(optional=True)
        Failover = T_BOOLEAN(default=False)
        common = T_SECTION(S_CHOICE, choices='sections', sections=[':common:config'] )
        cadmin = CAdminClientSettings()
        interface = Interface()
        routed = RoutedPortPairs()
        bridged = BridgedPortPairs()
        link = LinkedPortPairs()

    device = Device()

class Tunnelgroups(Section):
    '''
    Group of tunnels with common characteristics
    '''
    class Tunnelgroup(NSection):
        class Tunnel(Section):
            class TunnelEnd(Section):
                # DeviceOPattern = T_TEXT(S_CHOICE, choices=['Device', 'Pattern'], default='Device')
                # device = T_SECTION(S_CHOICE, choices='sections', sections=[':device:device'], conditions=['DeviceOPattern=Device'])
                # CNPattern = T_CN_PATTERN(conditions=['DeviceOPattern=Pattern'])
                device = T_SECTION(S_CHOICE, choices='sections', sections=[':device:device'])
                PortPair = T_ATOM(S_CHOICE, choices=portpair_extended)
                CNPattern = T_CN_PATTERN()
                AdminTunnel = T_BOOLEAN()

            Enable = T_BOOLEAN()
            Name = T_TEXT()
            A = TunnelEnd()
            B = TunnelEnd()

        class Multicasts(Section):
            class Grouprange(NSection):
                # Todo: T_MULTICAST_GROUP for From and To
                FromIP = T_IP_ADDRESS()
                ToIP = T_IP_ADDRESS()
            grouprange = Grouprange()

        Enable = T_BOOLEAN()
        Name = T_TEXT()
        Type = T_TEXT(S_CHOICE, choices=['Routed', 'Bridged', 'Link'])
        SoftLimit = T_DECIMAL(optional = True)
        HardLimit = T_DECIMAL(optional = True)
        #multicast = Multicasts()
        tunnel = Tunnel()

    tunnelgroup = Tunnelgroup()

class NetworkConfigration(Schema):
    certificate = CAs(display='CA')
    identity = Identities()
    common = CommonConfigs()
    device = Devices()
    tunnelgroup = Tunnelgroups()

conf = NetworkConfigration()

spec = conf.getSpec(2,0)
print
print(spec)

file = open("farist-vpn-net-3.0.spec", "w")
file.write(spec)
file.close()
