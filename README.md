# emcpy
Python Client for EMC NAS (Unity/VNX) Platforms

## Unity

### Supported Operations

| Resource | Get | Create | Modify | Delete |
| -------- | --- | ------ | ------ | ------ |
| cifsServer | x | x | x | x |
| dnsServer | | | | | |
| fileDNSServer | | | | | |
| fileInterface | | | | | |
| fileKerberosServer | | | | | |
| fileLDAPServer | | | | | |
| fileNDMPServer | | | | | |
| fileNISServer | | | | | |
| fsnPort | | | | | |
| ftpServer | | | | | |
| ipInterface | | | | | |
| ipPort | | | | | |
| iscsiNode | | | | | |
| iscsiPortal | | | | | |
| iscsiSettings | | | | | |
| linkAggregation | | | | | |
| mgmtInterface | | | | | |
| mgmtInterfaceSettings | | | | | |
| nasServer | | | | | |
| nfsServer | | | | | |
| preferredInterfaceSettings | | | | | |
| route | | | | | |
| smptServer | | | | | |
| tenant | | | | | |
| urServer | | | | | |
| virusChecker | | | | | |
| vlanInfo | | | | | |
| alert | | | | | |
| alertConfig | | | | | |
| alertConfigSMTPTarget | | | | | |
| alertEmailConfig | | | | | |
| event | | | | | |
| cifsShare | | | | | |
| datastore | | | | | |
| host | | | | | |
| hostContainer | | | | | |
| hostIPPort | | | | | |
| hostInitiator | | | | | |
| hostInitiatorPath | | | | | |
| hostLUN | | | | | |
| hostVVolDatastore | | | | | |
| nfsShare | | | | | |
| remoteSystem | | | | | |
| rpChapSettings | | | | | |
| vm | | | | | |
| vmDisk | | | | | |
| vmwarePE | | | | | |
| aclUser | | | | | |
| capabilityProfile | | | | | |
| dhsmConnection | | | | | |
| dhsmServer | | | | | |
| fastCache | | | | | |
| fastVP | | | | | |
| fileEventsPool | | | | | |
| fileEventsPublisher | | | | | |
| filesystem | | | | | |
| lun | | | | | |
| moveSession | | | | | |
| pool | | | | | |
| poolConsumer | | | | | |
| poolConsumerAllocation | | | | | |
| poolUnit | | | | | |
| quotaConfig | | | | | |
| storageResource | | | | | |
| storageResourceCapabilityProfile | | | | | |
| storageTier | | | | | |
| systemCapacity | | | | | |
| treeQuota | | | | | |
| userQuota | | | | | |
| virtualDisk | | | | | |
| virtualVolume | | | | | |
| dae | | | | | |
| disk | | | | | |
| dpe | | | | | |
| encryption | | | | | |
| ethernetPort | | | | | |
| kmipServer | | | | | |
| ssc | | | | | |
| ssd | | | | | |
| storageProcessor | | | | | |
| autodownloadSoftwareVersion | | | | | |
| basicSystemInfo | | | | | |
| candidateSoftwareVersion| | | | | |
| feature | | | | | |
| importSession | | | | | |
| installedSoftwareVersion | | | | | |
| license | | | | | |
| ntpServer | | | | | |
| remoteSyslog | | | | | |
| serviceContract | | | | | |
| softwareUpgradeSession | | | | | |
| system | | | | | |
| systemInformation | | | | | |
| systemLimit | | | | | |
| systemTime | | | | | |
| tbn | | | | | |
| tbnConfig | | | | | |
| upgradeSession | | | | | |
| archive | | | | | | 
| metric | | | | | | 
| metricCollection | | | | | | 
| metricQueryResult | | | | | | 
| metricRealTimeQuery | | | | | | 
| metricService | | | | | | 
| metricValue | | | | | | 
| ldapServer | | | | | |
| remoteInterface | | | | | |
| replicationInterface | | | | | |
| replicationSession | | | | | |
| snap | | | | | |
| snapSchedule | | | | | |
| ioLimitPolicy | | | | | |
| ioLimitRule | | | | | |
| ioLimitSetting | | | | | |
| configCaptureResult | | | | | |
| coreDump | | | | | |
| dataCollectionResult | | | | | |
| esrsParam | | | | | |
| esrsPolicyManager | | | | | |
| serviceAction | | | | | |
| serviceInfo | | | | | |
| supportAsset | | | | | |
| supportProxy | | | | | |
| supportService | | | | | |
| technicalAdvisory | | | | | |
| crl | | | | | |
| loginSessionInfo | | | | | |
| role | | | | | |
| roleMapping | | | | | |
| securitySettings | | | | | |
| user | | | | | |
| x509Certificate | | | | | |

### Import the module

`> from unity import unity`

### Define the object

`> nas = unity.Unity(hostname, user, password)`

### Log into the REST API

`> nas.connect()`

### Query a collection (filesystem)

`> nas.filesystem`

If you want to add parameters to the query use the `get` function.

`> nas.get('filesystem', fields='name,id', compact='true')`

### Query an instance (filesystem)

By name:

`> nas.get('filesystem', name='myFilesystem')`

Or by ID:

`> nas.get('filesystem', id='fs_3')`

### Create a NAS Server

`> nas.create('nasServer', 'cifs01', 'spa', 'pool_1')`

`cifs01` is the name of the NAS Server.
`spa` is the ID of the home Service Processor.
`pool_1` is the ID of the storage pool.

