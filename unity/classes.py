class Filesystem(object):
    def __init__(self, name, nasServer, size, poolId, **kwargs):
        fs = {
            'name': name,
            'replicationParameters': {
                'isReplicationDestination': isReplicationDestination
            },
            'snapScheduleParameters': {
                'snapSchedule': {
                    'id': snapSchedule
                }
            },
            'fsParameters': {
                'pool': {
                    'id': poolId
                },
                'nasServer': {
                    'id': nasServer
                },
                'supportedProtocols': supportedProtocols,
                'flrVersion': flrVersion,
                'flrMinRetention': flrMinRetention,
                'flrDefaultRetention': flrDefaultRetention,
                'flrMaxRetention': flrMaxRetention,
                'isFlrAutoLockEnabled': isFlrAutoLockEnabled,
                'isFlrAutoDeleteEnabled': isFlrAutoDeleteEnabled,
                'flrAutoLockDelay': flrAutoLockDelay,
                'errorThreshold': errorThreshold,
                'warningThreshold': warningThreshold,
                'infoThreshold': infoThreshold,
                'isThinEnabled': isThinEnabled,
                'isDataReductionEnabled': isDataReductionEnabled,
                'isAdvancedDedupEnabled': isAdvancedDedupEnabled,
                'size': size,
                'hostIOSize':
            },
            'cifsFsParameters': {},
            'nfsShareCreate': [],
            'cifsShareCreate': []
        }
    def do_nothing(self):
        pass