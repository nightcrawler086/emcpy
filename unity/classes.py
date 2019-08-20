class pool(object):
    def __init__(self, id):
        self.id = id


class nasServer(object):
    def __init__(self, id):
        self.id = id


class snapSchedule(object):
    def __init__(self, id):
        self.id = id


class snapScheduleParameters(snapSchedule):
    pass


class fsParameters(pool, nasServer):
    def __init__(self, size, **kwargs):
        if size[-1] is 'G':
            size_bytes = int(float(size[:-1]) * 1073741824)
        elif size[-1] is 'T':
            size_bytes = int(float(size[:-1]) * 1099511627776)
        else:
            print('Size must be specified like 1G (gigabytes) or 1T (terabytes)')
            return
        size = size_bytes
        self.__dict__.update(kwargs)
        super().__init__()


class replicationParameters(object):
    def __init__(self, isReplicationDestination):
        self.isReplicationDestination = isReplicationDestination


class cifsParameters(object):
    def __init__(self, isCIFSSyncWritesEnabled, isCIFSOpLocksEnabled, isCIFSNotifyOnWriteEnabled,
                 isCIFSNotifyOnAccessEnabled, cifsNotifyOnChangeDirDepth):
        self.isCIFSSyncWritesEnabled = isCIFSSyncWritesEnabled
        self.isCIFSOpLocksEnabled = isCIFSOpLocksEnabled
        self.isCIFSNotifyOnWriteEnabled = isCIFSNotifyOnWriteEnabled
        self.isCIFSNotifyOnAccessEnabled = isCIFSNotifyOnAccessEnabled
        self.cifsNotifyOnChangeDirDepth = cifsNotifyOnChangeDirDepth


class Filesystem(replicationParameters, snapSceduleParameters, fsParameters, cifsParameters):
    def __init__(self, name, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)




