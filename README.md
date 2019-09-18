# emcpy
Python Client for EMC NAS (Unity/VNX) Platforms

## Unity

### Supported Operations

| Resource | Get | Create | Modify | Delete | Supported Actions |
| -------- | --- | ------ | ------ | ------ | ----------------- |
| cifsServer | x | x | x | x | - |
| dnsServer | x | - | x | - | - |
| fileDNSServer | x | x | x | x | - |
| fileInterface | x | x | x | x | - |
| fileKerberosServer | x | x | x | x | - |
| fileLDAPServer | x | x | x | x | - |
| fileNDMPServer | x | x | x | x | - |
| fileNISServer | x | x | x | x | - |
| fsnPort | x | x | x | x |  |
| ftpServer | x | x | x | x | - |
| ipInterface | x | - | - | - | |
| ipPort | x | x | - | - | |
| iscsiNode | x | - | x | - | - |
| iscsiPortal | x | x | x | x | - |
| iscsiSettings | x | - | x | - | - |
| linkAggregation | x | x | x | x | |
| mgmtInterface | x | x | x | x | - |
| mgmtInterfaceSettings | x | - | x | - | - |
| nasServer | x | x | x | x | |
| nfsServer | x | x | x | x | - |
| preferredInterfaceSettings | x | - | | - | - |
| route | x | x | x | x | x |
| smtpServer | x | x | x | x | - |
| tenant | x | x | x | x | - |
| urServer | x | - | x | - | - |
| virusChecker | x | - | x | - | - |
| vlanInfo | x | - | - | - | - |
| vmwareNasPEServer | x | x | - | x | - |
| alert | x | | | | |
| alertConfig | x | | | | |
| alertConfigSMTPTarget | | | | | |
| alertEmailConfig | x | | | | |
| event | x | | | | |
| cifsShare | x | | | | |
| datastore | x | | | | |
| host | x | | | | |
| hostContainer | x | | | | |
| hostIPPort | x | | | | |
| hostInitiator | x | | | | |
| hostInitiatorPath | x | | | | |
| hostLUN | | | | | |
| hostVVolDatastore | x | | | | |
| nfsShare | x | | | | |
| remoteSystem | x | | | | |
| rpChapSettings | x | | | | |
| vm | x | | | | |
| vmDisk | x | | | | |
| vmwarePE | x | | | | |
| aclUser | x | | | | |
| capabilityProfile | x | | | | |
| dhsmConnection | x | | | | |
| dhsmServer | x | | | | |
| fastCache | | | | | |
| fastVP | x | | | | |
| fileEventsPool | x | | | | |
| fileEventsPublisher | x | | | | |
| filesystem | x | | | | |
| lun | x | | | | |
| moveSession | x | | | | |
| pool | x | | | | |
| poolConsumer | x | | | | |
| poolConsumerAllocation | x | | | | |
| poolUnit | x | | | | |
| quotaConfig | x | | | | |
| storageResource | x | | | | |
| storageResourceCapabilityProfile | x | | | | |
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

