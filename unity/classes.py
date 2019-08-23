import json


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


class pool(object):
    def __init__(self, poolId):
        self.id = poolId


class nasServer(object):
    def __init__(self, nasServerId):
        self.id = nasServerId


class replicationParameters(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class snapScheduleParameters(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class snapSchedule(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class cifsFileSystemParameters:
    def __init__(self, **kwargs):
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
        self.fsParameters.pool = pool(poolId)
        self.fsParameters.nasServer = nasServer(nasServerId)
        for k, v in kwargs.items():
            if k in fs_params:
                self.fsParameters.__setattr__(k, v)
            elif k in rep_params:
                self.replicationParameters = replicationParameters()
                self.replicationParameters.__setattr__(k, v)
            elif k in snap_params:
                if k is 'snapSchedule':
                    self.snapScheduleParameters = snapScheduleParameters()
                    self.snapScheduleParameters.snapSchedule = snapSchedule()
                    self.snapScheduleParameters.snapSchedule.__setattr__(k, v)
                else:
                    self.snapScheduleParameters.__setattr__(k, v)
            elif k in cifs_params:
                if 'cifsFsParameters' not in self.__dict__:
                    self.cifsFsParameters = cifsFileSystemParameters()
                    self.cifsFsParameters.__setattr__(k, v)
                else:
                    self.cifsFsParameters.__setattr__(k, v)

    def jsonify(self):
        json_data = json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data
