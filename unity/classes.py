class StorageResource(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Filesystem(object):
    def __init__(self, name, nasServer, size, pool, **kwargs):
        self.name = name
        self.nasServer = nasServer
        self.size = size
        self.pool = pool
        self.__dict__.update(kwargs)


class ReplicationParameters(object):
    def __init__(self, isReplicationDestination):
        self.isReplicationDestination = isReplicationDestination

