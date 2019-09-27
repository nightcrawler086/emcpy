class IdObject(object):
    """
    This is a simple class, that is used for multiple objects.  Many
    of the data objects we create require a related ID of another object.

    For instance:

    If I was going to create a filesystem, I would define the filesystem object.
    In order to create a filesystem, you need to specify the ID of he NAS Server
    on which to create it.  So, in building the filesystem object (which needs to
    be converted to JSON), you need a property for the NAS Server, which is a
    nested ID object.  We use this one to define the ID object for any object
    like that instead of having too similar class names
    (ex. NasServer and NasServerId)
    """
    def __init__(self, oId):
        self.id = oId


class OptObject(object):
    """
    This class is used for all optional parameters.  It only updates itself
    with everything from **kwargs.

    For instance:

    If I was going to create a filesystem, I would define the filesystem object.
    If I wanted to specify that this filesystem is a replication destination,
    then I would need a nested object named 'replicationParameters'.  Inside the
    class that builds the filesystem object, if the 'isReplicationDestination'
    keyword argument is given, then I'll define this class in a
    'replicationParameters' property on the filesystem object.  This will allow
    the object to be converted to JSON in the correct format.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Configuring network communication


class cifsServer:
    def __init__(self, nasServerId, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.__dict__.update(kwargs)


class fileDNSServer:
    def __init__(self, nasServerId, domain, addrList: list):
        self.nasServer = IdObject(nasServerId)
        self.domain = domain
        self.addresses = addrList


class fileInterface:
    def __init__(self, nasServerId, ipPortId, ipAddress, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.ipPort = IdObject(ipPortId)
        self.ipAddress = ipAddress
        self.__dict__.update(kwargs)


class fileKeberosServer:
    def __init__(self, nasServerId, realm, addresses, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.realm = realm
        self.addresses = addresses


class fileLDAPServer:
    def __init__(self, nasServerId, authenticationType, authority, serverAddresses: list, **kwargs):
        """

        :param nasServerId: ID of the NAS Server on which to create
        :param authenticationType: From AuthenticationTypeEnum:
                                    0 = Anonymous
                                    1 = Simple
                                    2 = Kerberos
        :param authority:  The Base DN
        :param serverAddresses:  List of LDAP Server addresses.
        :param kwargs: All other arguments are keyword
        """
        self.nasServer = IdObject(nasServerId)
        self.authenticationType = authenticationType
        self.authority = authority
        self.serverAddresses = serverAddresses
        self.__dict__.update(kwargs)


class fileNDMPServer:
    def __init__(self, nasServerId, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.__dict__.update(kwargs)


class fileNISServer:
    def __init__(self, nasServerId, domain, addresses: list):
        self.nasServer = IdObject(nasServerId)
        self.domain = domain
        self.addresses = addresses


class fsnPort:
    def __init__(self, primaryPort, secondaryPorts: list, **kwargs):
        self.primaryPort = IdObject(primaryPort)
        self.secondaryPorts = secondaryPorts
        self.__dict__.update(kwargs)


class ftpServer:
    def __init__(self, nasServerId, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.__dict__.update(kwargs)


class iscsiPortal:
    def __init__(self, ethernetPortId, ipAddress: list, **kwargs):
        self.ethernetPort = IdObject(ethernetPortId)
        self.ipAddress = ipAddress
        self.__dict__.update(kwargs)


class linkAggregation:
    def __init__(self, ports: list, **kwargs):
        self.ports = ports
        self.__dict__.update(kwargs)


class mgmtInterface:
    def __init__(self, ipAddress, **kwargs):
        self.ipAddress = ipAddress
        self.__dict__.update(kwargs)


class nasServer:
    def __init__(self, name, homeSP, poolId, **kwargs):
        self.name = name
        self.homeSP = IdObject(homeSP)
        self.pool = IdObject(poolId)
        for k, v in kwargs.items():
            if k == 'tenant':
                self.tenant = IdObject(v)
            else:
                self.__setattr__(k, v)


class nfsServer:
    def __init__(self, nasServerId, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.__dict__.update(kwargs)


class route:
    def __init__(self, ipInterface, **kwargs):
        self.ipInterface = IdObject(ipInterface)
        self.__dict__.update(kwargs)


class smtpServer:
    def __init__(self, address, type, **kwargs):
        """

        :param address: address of the SMTP server
        :param type:  SMTP Server type
                        0 = Default
                        1 = PhoneHome
        """
        self.address = address
        self.type = type
        self.__dict__.update(kwargs)


class tenant:
    def __init__(self, name, vlans: list, **kwargs):
        self.name = name
        self.vlans = vlans
        self.__dict__.update(kwargs)


class vmwareNasPEServer:
    def __init__(self, nasServerId, fileInterfaces: list):
        self.nasServer = IdObject(nasServerId)
        self.fileInterfaces = fileInterfaces




# Managing events and alerts


class alertConfigSNMPTarget:
    def __init__(self, targetAddress, **kwargs):
        self.targetAddress = targetAddress
        self.__dict__.update(kwargs)


class alertEmailConfig:
    def __init__(self, emailAddress, **kwargs):
        self.emailAddress = emailAddress
        self.__dict__.update(kwargs)


# Managing jobs


class job:
    def __init__(self, description, tasks: list, **kwargs):
        self.description = description
        self.tasks = tasks
        self.__dict__.update(kwargs)


# Managing remote systems


class cifsShare:
    def __init__(self, snapId, path, name, **kwargs):
        self.snap = IdObject(snapId)
        self.path = path
        self.name = name
        self.__dict__.update(kwargs)


class host:
    def __init__(self, type, name, **kwargs):
        self.type = type
        self.name = name
        self.__dict__.update(kwargs)


class hostContainer:
    """
    """
    def __init__(self, serviceType, targetName, targetAddress, username, password, **kwargs):
        vasa_params = {'localUsername', 'localPassword'}
        self.serviceType = serviceType
        self.targetName = targetName
        self.targetAddress = targetAddress
        self.username = username
        self.password = password
        for k, v in kwargs.items():
            if k in vasa_params:
                if not hasattr(self, 'vasaProviderParameters'):
                    self.vasaProviderParameters = OptObject()
                self.vasaProviderParameters.__setattr__(k, v)
            else:
                self.__setattr__(k, v)


class hostIPPort:
    def __init__(self, hostId, address, **kwargs):
        self.host = IdObject(hostId)
        self.address = address
        self.__dict__.update(kwargs)


class hostInitiator:
    def __init__(self, hostId, initiatorType, initiatorWWNorIqn, **kwargs):
        self.host = IdObject(hostId)
        self.initiatorType = initiatorType
        self.initiatorWWNorIqn = initiatorWWNorIqn
        self.__dict__.update(kwargs)


class nfsShare:
    def __init__(self, snapId, path, name, **kwargs):
        self.snap = IdObject(snapId)
        self.path = path
        self.name = name
        self.__dict__.update(kwargs)


class remoteSystem:
    def __init__(self, managementAddress, **kwargs):
        self.managementAddress = managementAddress
        self.__dict__.update(kwargs)


# Managing storage


class capabilityProfile:
    def __init__(self, name, pool, **kwargs):
        self.name = name
        self.pool = pool
        self.__dict__.update(kwargs)


class dhsmConnection:
    def __init__(self, secondaryUrl, filesystemId, **kwargs):
        self.secondaryUrl = secondaryUrl
        self.filesystemId = filesystemId
        self.__dict__.update(kwargs)


class dhsmServer:
    def __init__(self, nasServerId, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.__dict__.update(kwargs)


class fileEventsPool:
    def __init__(self, eventsPublisherId, name, servers: list, **kwargs):
        self.eventsPublisher = IdObject(eventsPublisherId)
        self.name = name
        self.servers = servers
        self.__dict__.update(kwargs)


class moveSession:
    def __init__(self, sourceStorageResourceId, destinationPoolId, **kwargs):
        self.sourceStorageResource = IdObject(sourceStorageResourceId)
        self.destinationPool = IdObject(destinationPoolId)
        self.__dict__.update(kwargs)


class pool:
    def __init__(self, name, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)


class treeQuota:
    def __init__(self, filesystemId, path, **kwargs):
        self.filesystem = IdObject(filesystemId)
        self.path = path
        self.__dict__.update(kwargs)


## Storage resources (LUN, ConsistencyGroup, VMwareLun, VMwareNFS, Filesystem, VVol

class lunParameters:
    """
    @todo - Not complete yet
    """
    def __init__(self, size, **kwargs):
        if size[-1] is 'G':
            size_bytes = int(float(size[:-1]) * 1073741824)
        elif size[-1] is 'T':
            size_bytes = int(float(size[:-1]) * 1099511627776)
        else:
            print('Size must be specified like 1G (gigabytes) or 1T (terabytes)')
            return
        self.size = size_bytes


class Lun:
    """
    @todo - incomplete
    """
    def __init__(self, name, poolId, size, **kwargs):
        self.name = name
        lun_params = {'isThinEnabled', 'isDataReductionEnabled', 'isAdvancedDedupEnabled',
                      'defaultNode', 'hostAccess'}
        rep_params = {'isReplicationDestination'}
        snap_params = {'snapSchedule', 'isSnapSchedulePaused'}
        fastvp_params = {'tieringPolicy'}
        self.lunParameters = lunParameters(size)
        self.lunParameters.pool = IdObject(poolId)


class fsParameters(object):
    def __init__(self, size, **kwargs):
        if size[-1] is 'G':
            size_bytes = int(float(size[:-1]) * 1073741824)
        elif size[-1] is 'T':
            size_bytes = int(float(size[:-1]) * 1099511627776)
        else:
            print('Size must be specified like 1G (gigabytes) or 1T (terabytes)')
            return
        self.size = size_bytes
        self.__dict__.update(kwargs)


class Filesystem:
    def __init__(self, name, poolId, nasServerId, size, **kwargs):
        self.name = name
        fs_params = {'supportedProtocols', 'flrVersion', 'flrMinRetention', 'flrDefaultRetention',
                     'flrMaxRetention', 'isFlrAutoLockEnabled', 'isFlrAutoDeleteEnabled', 'flrAutoLockDelay',
                     'errorThreshold', 'warningThreshold', 'infoThreshold', 'isThinEnabled',
                     'isDataReductionEnabled', 'isAdvancedDedupEnabled', 'size', 'hostIOSize',
                     'sizeAllocated', 'minSizeAllocated', 'isCacheDisabled', 'accessPolicy',
                     'folderRenamePolicy', 'lockingPolicy', 'poolFullPolicy'}
        rep_params = {'isReplicationDestination'}
        snap_params = {'snapSchedule', 'isSnapSchedulePaused'}
        cifs_params = {'isCIFSSyncWritesEnabled', 'isCIFSOpLocksEnabled', 'isCIFSNotifyOnWriteEnabled',
                       'isCIFSNotifyOnAccessEnabled', 'cifsNotifyOnChangeDirDepth'}
        self.fsParameters = fsParameters(size)
        self.fsParameters.pool = IdObject(poolId)
        self.fsParameters.nasServer = IdObject(nasServerId)
        for k, v in kwargs.items():
            if k in fs_params:
                self.fsParameters.__setattr__(k, v)
            elif k in rep_params:
                if not hasattr(self, 'replicationParameters'):
                    self.replicationParameters = OptObject()
                self.replicationParameters.__setattr__(k, v)
            elif k in snap_params:
                if k is 'snapSchedule':
                    self.snapScheduleParameters = OptObject()
                    self.snapScheduleParameters.snapSchedule = OptObject()
                    self.snapScheduleParameters.snapSchedule.__setattr__(k, v)
                else:
                    self.snapScheduleParameters.__setattr__(k, v)
            elif k in cifs_params:
                if not hasattr(self, 'cifsFsParameters'):
                    self.cifsFsParameters = OptObject()
                    self.cifsFsParameters.__setattr__(k, v)
                else:
                    self.cifsFsParameters.__setattr__(k, v)
            else:
                self.__setattr__(k, v)


class userQuota:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Managing the environment

class kmipServer:
    def __init__(self, addresses: list, port, timeout, username, password):
        self.addresses = addresses
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password


# Managing the system

class remoteSyslog:
    def __init__(self, address, **kwargs):
        self.address = address
        self.__dict__.update(kwargs)


## Under Managing the environment, the following resources need classes:
##      importSession, softwareUpgradeSession, upgradeSession

# Protecting data

class ldapServer:
    def __init__(self, bindDN, bindPassword, userSearchPath, groupSearchPath, **kwargs):
        self.bindDN = bindDN
        self.bindPassword = bindPassword
        self.userSearchPath = userSearchPath
        self.groupSearchPath = groupSearchPath
        self.__dict__.update(kwargs)


class replicationInterface:
    def __init__(self, sp, ipPort, ipAddress):
        self.sp = IdObject(sp)
        self.ipPort = IdObject(ipPort)
        self.ipAddress = ipAddress
        self.__dict__.update(kwargs)


class replicationSession:
    def __init__(self, srcResourceId, dstResourceId, maxTimeOutOfSync, hourlySnapReplicationPolicy: dict = None,
                 dailySnapReplicationPolicy: dict = None, **kwargs):
        id_objects = {'srcSPAInterface', 'srcSPBInterface', 'dstSPAInterface', 'dstSPBInterface'}
        self.srcResourceId = srcResourceId
        self.dstResourceId = dstResourceId
        self.maxTimeOutOfSync = maxTimeOutOfSync
        for k, v in kwargs.items():
            if k in id_objects:
                self.__setattr__(k, IdObject(v))


class snap:
    def __init__(self, storageResource, **kwargs):
        self.storageResource = IdObject(storageResource)
        self.__dict__.update(kwargs)


class snapSchedule:
    def __index__(self, name: str, rules: list, **kwargs):
        self.name = name
        self.rules = rules
        self.__dict__.update(kwargs)


class roleMapping:
    def __init__(self, authorityName: str, entityName: str, roleName: str, mappingType: enum):
        """

        :param authorityName:
        :param entityName:
        :param roleName:
        :param mappingType: 0 - ldapgroup - LDAP Group role.
                            1 - ldapuser - LDAP User role.
                            2 - localuser - Local User role.
                            3 - unknown - Unknown role type.
        """
        self.authorityName = authorityName
        self.entityName = entityName
        self.roleName = roleName
        self.mappingType = mappingType


class user:
    def __init__(self, user, role, password):
        self.user = user
        self.role = role
        self.password = password

