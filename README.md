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
| storageTier | x | | | | |
| systemCapacity | x | | | | |
| treeQuota | x | | | | |
| userQuota | x | | | | |
| virtualDisk | x | | | | |
| virtualVolume | x | | | | |
| dae | x | | | | |
| disk | x | | | | |
| dpe | x | | | | |
| encryption | x | | | | |
| ethernetPort | x | | | | |
| kmipServer | x | | | | |
| ssc | x | | | | |
| ssd | x | | | | |
| storageProcessor | x | | | | |
| autodownloadSoftwareVersion | x | | | | |
| basicSystemInfo | x | | | | |
| candidateSoftwareVersion | x | | | | |
| feature | x | | | | |
| importSession | x | | | | |
| installedSoftwareVersion | x | | | | |
| license | x | | | | |
| ntpServer | x | | | | |
| remoteSyslog | x | | | | |
| serviceContract | x | | | | |
| softwareUpgradeSession | x | | | | |
| system | x | | | | |
| systemInformation | x | | | | |
| systemLimit | x | | | | |
| systemTime | x | | | | |
| tbn | x | | | | |
| tbnConfig | x | | | | |
| upgradeSession | x | | | | |
| archive | x | | | | | 
| metric | | | | | | 
| metricCollection | | | | | | 
| metricQueryResult | | | | | | 
| metricRealTimeQuery | | | | | | 
| metricService | | | | | | 
| metricValue | | | | | | 
| ldapServer | x | | | | |
| remoteInterface | x | | | | |
| replicationInterface | x | | | | |
| replicationSession | x | | | | |
| snap | x | | | | |
| snapSchedule | x | | | | |
| ioLimitPolicy | x | | | | |
| ioLimitRule | x | | | | |
| ioLimitSetting | x | | | | |
| configCaptureResult | | | | | |
| coreDump | | | | | |
| dataCollectionResult | | | | | |
| esrsParam | x | | | | |
| esrsPolicyManager | x | | | | |
| serviceAction | x | | | | |
| serviceInfo | x | | | | |
| supportAsset | x | | | | |
| supportProxy | x | | | | |
| supportService | x | | | | |
| technicalAdvisory | x | | | | |
| crl | x | | | | |
| loginSessionInfo | x | | | | |
| role | x | | | | |
| roleMapping | x | | | | |
| securitySettings | x | | | | |
| user | x | | | | |
| x509Certificate | x | | | | |

### Usage

#### Import the module

`> from unity import unity`

#### Instantiate the class

`> nas = unity.Unity(hostname, user, password)`

### Login to the REST API

`> nas.connect()`

OR

`> nas.connect(quiet=True)`


### Queries

Most queries can be done through the `get` function.

#### Collection Query

`> nas.get('resourceName')`

You can specify the fields to retrieve:

`> nas.get('resourceName', fields='field1,field2')`

#### Instance Query

You can query an instance by ID:

`> nas.get('resourceName', rid='resourceId')`

Or by name:

`> nas.get('resourceName', rname='resourceName')`

Both instance queries (by ID or Name) take the same field selections:

`> nas.get('resourceName', rname='resourceName', fields='field1,field2')`


