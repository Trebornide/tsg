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
portpair_extended = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '2.1', '2.2', '2.3', '2.4', 'Admin', 'MacSecAll']

class CAs(Section):
    '''
    CA used by device.
    '''
    class CA(NSection):
        Name = T_TEXT(optional=True)
        CN   = T_CN_PATTERN()
        Location = T_ATOM(S_CHOICE , choices=['Config', 'File', 'Card'])
        PEM  = T_PEM(display='PEM file', conditions=['Location==Config'], optional=True)
        CRL = T_URL(optional=True)

    # ca = CA(max=32, linkdisplay=['CN'])
    ca = CA(max=32)

class Identities(Section):
    '''
    Administrative identities to manage the devices 
    '''
    class Options():
        display='Administrators'

    class Identity(NSection):
        Name  = T_TEXT(title='Admin group name', optional=True)
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
            Administrator = T_SECTION(S_CHOICE, choices='sections', sections=[':identity:identity'], optional=True)
            Operator      = T_SECTION(S_CHOICE, choices='sections', sections=[':identity:identity'], optional=True)

        class Certificates(Section):
            AllowedCA = T_SECTION(S_CHOICE_MULTI, max=32, choices='sections', sections=[':certificate:ca'])
            AllowExpiredCert = T_BOOLEAN(default=False)

        class Syslog(Section):
            '''
            Syslog
            '''
            class Remote(NSection):
                Enable = T_BOOLEAN(default=True)
                Host = T_DOMAIN_NAME()
                Protocol = T_ATOM(S_CHOICE, choices=['TCP', 'UDP'], default='TCP')
                Level = T_ATOM(S_CHOICE, choices=['Debug', 'Info', 'Warning', 'Error'], default='Info')

            Storage = T_ATOM(S_CHOICE, choices=['Transient', 'Permanent'], default='Transient')
            History = T_DECIMAL(min=1, max=365, default=90)
            Remote = Remote(max=5)

        class SyslogOld:
            '''
            Syslog
            '''
            Enable = T_BOOLEAN(default=False)
            Server = T_IP_REDUCED(S_LIST, max=5)

        class General(Section):
            '''
            General
            '''
            TimeZone = T_ATOM(S_CHOICE, choices=time_zones, optional=True)

        class NTP(Section):
            '''
            Network Time Protocol
            '''
            class Key(NSection):
                Name = T_TEXT(optional=True)
                Number = T_DECIMAL()
                Key = T_ATOM()

            class Server(NSection):
                Name = T_TEXT(optional=True)
                Server = T_DOMAIN_NAME()
                Key = T_SECTION(S_CHOICE, choices='section', section=[':common:config:ntp:key'], optional=True)

            Enable = T_BOOLEAN(default=False)
            Key = Key(max=5)
            Server = Server(max=5)

        class SNMP(Section):
            '''
            SNMP
            '''
            Enable = T_BOOLEAN(default=False)
            TrapHost = T_DOMAIN_NAME(S_LIST, max=5)

        class AutoUpdate(Section):
            '''
            AutoUpdate
            '''
            Enable = T_BOOLEAN(default=False)
            BaseURL = T_URL()
            Timeout = T_DECIMAL(optional=True)

        class CRLUpdate(Section):
            '''
            CRLUpdate
            '''
            Enable = T_BOOLEAN(default=False)
            Timeout = T_DECIMAL(optional=True)

        class Resolver(Section):
            '''
            Resolver
            '''
            Enable = T_BOOLEAN(default=False)
            Address = T_IP_REDUCED(S_LIST, max=5)

        class Tunnel(Section):
            '''
            Tunnel
            '''
            Port = T_PORT(default=443, optional = True)
            LogDroppedBroadcast = T_BOOLEAN(optional=True, default=False)


        Name    = T_TEXT(optional=True)
        cadmin  = CAdmin(display='CAdmin server settings')
        cert    = Certificates(display='CA certificates')
        #syslog  = SyslogOld()
        syslog  = Syslog(display='Syslog')
        general = General(display='General')
        ntp     = NTP(display='NTP')
        snmp    = SNMP(display='SNMP')
        autoupdate = AutoUpdate(display='FW auto update')
        crlupdate = CRLUpdate(display='CRL update')
        resolver = Resolver(display='Address resolver')
        tunnel = Tunnel(display='Misc common tunnel settings')

    config = CommonConfig()


class Credentials(Section):
    '''
    Credentials
    '''
    Location = T_ATOM(S_CHOICE_MULTI, choices=['Card', 'File'], default='File')

class CAdminClientSettings(Section):
    '''
    Cadmin Client Settings
    '''
    CN = T_CN()
    Address = T_DOMAIN_NAME(S_LIST, max=2, optional=True)
    PollInterval = T_DECIMAL(default=10, optional=True)
    Port = T_PORT(default=443, optional=True)

class Networks(NSection):
    class Options:
        max=1024

    Enable  = T_BOOLEAN(default=False)
    '''Network'''
    Enable  = T_BOOLEAN(default=True)
    Name    = T_TEXT(optional=True)
    Address = T_IP_ADDRESS(mask=True)
    Gateway = T_IP_REDUCED()

class DHCP(Section):
    Enable        = T_BOOLEAN(default=False)
    '''DHCP'''
    Enable        = T_BOOLEAN(default=True)
    DNS           = T_BOOLEAN(default=False)
    DefaultRouter = T_BOOLEAN(default=False)

class RoutedInterface(Section):
    Address  = T_IP_ADDRESS(mask=True)
    MTU      = T_DECIMAL(optional=True)
    Network  = Networks()

class RoutedInterfaceDHCP(Section):
    Address  = T_IP_ADDRESS(mask=True, optional=True)
    MTU      = T_DECIMAL(optional=True)
    Network  = Networks()
    DHCP     = DHCP(optional=True)

class LinkInterface(Section):
    MTU      = T_DECIMAL(optional=True)

class Filters(Section):
    '''
    Filters
    '''
    class Filter(NSection):
        # ToDo: OneOf filter type in the future
        Enable = T_BOOLEAN(default=True)
        Name = T_TEXT(optional=True)
        FilterType = T_ATOM(S_CHOICE, choices=['NTP'], default='NTP')
        PortPair = T_PORTPAIR(S_CHOICE, choices=portpair)
        ClearNTP = T_IP_REDUCED()
        CryptoNTP = T_IP_REDUCED()
    Filter = Filter()


class Multicasts(Section):
    '''
    Multicast
    '''

    class Grouprange(NSection):
        Enable = T_BOOLEAN(default=True)
        FromIP = T_MULTICAST_GROUP()
        ToIP = T_MULTICAST_GROUP()

    grouprange = Grouprange()


class RoutedPortPairs(Section):
    '''
    Routed Crypto function
    '''

    class RoutedPortPair(NSection):
        Enable = T_BOOLEAN(default=True)
        Name = T_TEXT(optional=True)
        PortPair = T_PORTPAIR(S_CHOICE, choices=portpair)
        TunnelForwarding = T_BOOLEAN(default=False)
        FailoverPair = T_PORTPAIR(S_CHOICE,
                                  choices=portpair,
                                  conditions=['../../interface/failover/enable==true'],
                                  optional=True)
        clear = RoutedInterface(display='Clear text')
        crypto = RoutedInterfaceDHCP(display='Crypto text')
        # multicast = Multicasts()

    portpair = RoutedPortPair()

class BridgedPortPairs(Section):
    ''' 
    Bridged Crypto function
    '''
    class BridgedPortPair(NSection):
        Enable = T_BOOLEAN(default=True)
        Name = T_TEXT(optional=True)
        PortPair = T_PORTPAIR(S_CHOICE, choices=portpair)
        FailoverPair = T_PORTPAIR(S_CHOICE,
                                  choices=portpair,
                                  conditions=['../../interface/failover/enable==true'],
                                  optional=True)
        clear = LinkInterface(display='Clear text')
        crypto = RoutedInterfaceDHCP(display='Crypto text')
    portpair = BridgedPortPair()

class LinkedPortPairs(Section):
    '''
    Link Crypto function
    '''
    class LinkedPortPair(NSection):
        Enable = T_BOOLEAN(default=True)
        Name = T_TEXT(optional=True)
        PortPair = T_PORTPAIR(S_CHOICE, choices=portpair)
        FailoverPair = T_PORTPAIR(S_CHOICE,
                                  choices=portpair,
                                  conditions=['../../interface/failover/enable==true'],
                                  optional=True)
        MTU      = T_DECIMAL(optional=True)
    portpair = LinkedPortPair()

class Interface(Section):
    '''
    Interfaces
    '''
    class ManagementInterface(Section):
        '''
        Management 
        '''
        Enable = T_BOOLEAN(default=True)
        Name = T_TEXT(optional=True)
        Address = T_IP_ADDRESS(mask=True, optional=True)
        Network  = Networks()
        MTU = T_DECIMAL(optional=True, default=1500)
        DHCP = DHCP(optional=True)

    class FailoverManagementInterface(Section):
        '''
        Failover
        '''
        class Interface(Section):
            Address = T_IP_REDUCED(mask=True)
            MAC = T_ETHERNET_ADDRESS()

        class VirtualServer(Section):
            Vhid = T_DECIMAL()
            Key = T_ATOM()

        class FailoverPortPairSettings(Section):
            GraceTime = T_DECIMAL()

        Enable = T_BOOLEAN(default=False)
        MTU = T_DECIMAL(default=1500)
        primary = Interface(display='Device 1 management interface')
        secondary = Interface(display='Device 2 management interface')
        network = Networks()
        virtualserver = VirtualServer()
        portpair = FailoverPortPairSettings(optional=True)

    mgmt = ManagementInterface(display='Management')
    #mgmt2 = ManagementInterface()
    failover = FailoverManagementInterface(display='Failover')

class Devices(Section):
    '''
    Färist VPN-devices
    '''
    class Options():
        display='VPN devices'

    class Device(NSection):
        Name = T_TEXT(optional=True)
        Enable = T_BOOLEAN(default=False)
        DeviceType = T_ATOM(S_CHOICE, choices=farist4_models)
        Version = T_ATOM(S_CHOICE, choices=['PGAI 4.0.5', 'PGAI 4.1', 'PGAI 4.2'], default='PGAI 4.1')
        Hostname = T_DOMAIN_NAME(optional=True)
        # Failover = T_BOOLEAN(default=False)
        CommonConfig = T_SECTION(S_CHOICE, choices='sections', sections=[':common:config'] )

        credentials = Credentials(display='Credentials')
        cadmin = CAdminClientSettings(display='CAdmin client Settings')
        interface = Interface(display='Management')
        routed = RoutedPortPairs(display='Routed')
        bridged = BridgedPortPairs(display='Bridged')
        link = LinkedPortPairs(display='Link')
        filter = Filters(display='Filter')

    device = Device()

class Tunnelgroups(Section):
    '''
    Group of tunnels with common characteristics
    '''
    class Tunnelgroup(NSection):

        class Tunnels(NSection):
            '''
            Tunnels
            '''
            class TunnelEnd(Section):
                # DeviceOPattern = T_TEXT(S_CHOICE, choices=['Device', 'Pattern'], default='Device')
                # device = T_SECTION(S_CHOICE, choices='sections', sections=[':device:device'], conditions=['DeviceOPattern=Device'])
                # CNPattern = T_CN_PATTERN(conditions=['DeviceOPattern=Pattern'])
                Device = T_SECTION(S_CHOICE, choices='sections', sections=[':device:device'], optional=True)
                CNPattern = T_CN_PATTERN(conditions=['Device==null'], optional=True)
                PortPair = T_ATOM(S_CHOICE, choices=portpair_extended)
                # AdminTunnel = T_BOOLEAN(conditions=['PortPair=="1.1"', '../../Type=="Routed"'], optional=True)

            Enable = T_BOOLEAN(default=True)
            Name = T_TEXT(optional=True)
            A = TunnelEnd()
            B = TunnelEnd()

        Enable = T_BOOLEAN(default=True)
        Name = T_TEXT(optional=True)
        Type = T_ATOM(S_CHOICE, choices=['Routed', 'Bridged', 'Link'])
        SoftLimit = T_DECIMAL(optional = True)
        HardLimit = T_DECIMAL(optional = True)
        MTU = T_DECIMAL(optional=True)
        multicast = Multicasts(conditions=['../Type=="Routed"'], optional=True)
        tunnel = Tunnels()

    group = Tunnelgroup()

class NetworkConfigration(Schema):
    certificate = CAs(display='CA')
    identity = Identities()
    common = CommonConfigs()
    device = Devices()
    group = Tunnelgroups(display='Tunnel groups')

conf = NetworkConfigration()

spec = conf.getSpec(3,0)
print
print(spec)

file = open("farist-vpn-net-3.0.beta.spec", "w", newline='\n')
file.write(spec)
file.close()

schema = conf.getSchema(indent=2)
schema_file = open("farist-vpn-net-3.0.schema.json", "w", newline='\n')
schema_file.write(schema)
schema_file.close()

