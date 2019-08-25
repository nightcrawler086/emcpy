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


class optObject(object):
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


class StorageResourceFilesystem:
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
        self.fsParameters.nasServer = idObject(nasServerId)
        for k, v in kwargs.items():
            if k in fs_params:
                self.fsParameters.__setattr__(k, v)
            elif k in rep_params:
                self.replicationParameters = optObject()
                self.replicationParameters.__setattr__(k, v)
            elif k in snap_params:
                if k is 'snapSchedule':
                    self.snapScheduleParameters = optObject()
                    self.snapScheduleParameters.snapSchedule = optObject()
                    self.snapScheduleParameters.snapSchedule.__setattr__(k, v)
                else:
                    self.snapScheduleParameters.__setattr__(k, v)
            elif k in cifs_params:
                if 'cifsFsParameters' not in self.__dict__:
                    self.cifsFsParameters = optObject()
                    self.cifsFsParameters.__setattr__(k, v)
                else:
                    self.cifsFsParameters.__setattr__(k, v)


class cifsServer:
    def __init__(self, nasServerId, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.__dict__.update(kwargs)


class fileDNSServer:
    def __init__(self, nasServerId, domain, addrList):
        self.nasServer = IdObject(nasServerId)
        self.domain = domain
        if type(addrList) == list:
            self.addresses = addrList
        else:
            self.addresses = addrList.split(',')


class fileInterface:
    def __init__(self, nasServerId, ipPortId, ipAddress, **kwargs):
        self.nasServer = IdObject(nasServerId)
        self.ipPort = IdObject(ipPortId)


