# emcpy
Python Client for EMC NAS (Unity/VNX) Platforms

## Unity

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


### Supported Operations

| Resource | Get | Create | Modify | Delete | Supported Actions |
| -------- | --- | ------ | ------ | ------ | ----------------- |
| cifsServer | y | x | y | y | - |
| dnsServer | y | - | y | - | - |
| fileDNSServer | y | y | y | y | - |
| fileInterface | y | y | y | y | - |
| fileKerberosServer | y | y | y | y | - |
| fileLDAPServer | y | y | y | y | - |
| fileNDMPServer | y | y | y | y | - |
| fileNISServer | y | y | y | y | - |
| fsnPort | y | y | y | y | recommendForInterface |
| ftpServer | y | y | y | y | - |
| ipInterface | y | - | - | - | |
| ipPort | y | y | - | - | |
| iscsiNode | y | - | y | - | - |
| iscsiPortal | y | y | y | y | - |
| iscsiSettings | y | - | y | - | - |
| linkAggregation | y | y | y | y | |
| mgmtInterface | y | y | y | y | - |
| mgmtInterfaceSettings | y | - | y | - | - |
| nasServer | y | y | y | y | Ping, PingByName, Traceroute, TracerouteByName, generateUserMappingsReport, generateUserMappingsReportByName, UpdateUserMappings, UpdateUserMappingsByName|
| nfsServer | y | y | y | y | - |
| preferredInterfaceSettings | y | - | | - | - |
| route | y | y | y | y | y |
| smtpServer | y | y | y | y | - |
| tenant | y | y | y | y | - |
| urServer | y | - | y | - | - |
| virusChecker | y | - | y | - | - |
| vlanInfo | y | - | - | - | - |
| vmwareNasPEServer | y | y | - | y | - |
| alert | y | | | | |
| alertConfig | y | | | | |
| alertConfigSMTPTarget | y | y | | | |
| alertEmailConfig | y | y | | | |
| job | y | y | | | |
| event | y | | | | |
| cifsShare | y | y | | | |
| datastore | y | | | | |
| host | y | y | | | |
| hostContainer | y | y | | | |
| hostIPPort | y | y | | | |
| hostInitiator | y | y | | | |
| hostInitiatorPath | y | | | | |
| hostLUN | | | | | |
| hostVVolDatastore | y | | | | |
| nfsShare | y | y | | | |
| remoteSystem | y | y | | | |
| rpChapSettings | y | | | | |
| vm | y | | | | |
| vmDisk | y | | | | |
| vmwarePE | y | | | | |
| aclUser | y | | | | |
| capabilityProfile | y | y | | | |
| dhsmConnection | y | y | | | |
| dhsmServer | y | y | | | |
| fastCache | | | | | |
| fastVP | y | | | | |
| fileEventsPool | y | y | | | |
| fileEventsPublisher | y | | | | |
| filesystem | y | | | | |
| lun | y | | | | |
| moveSession | y | y | | | |
| pool | y | y | | | |
| poolConsumer | y | | | | |
| poolConsumerAllocation | y | | | | |
| poolUnit | y | | | | |
| quotaConfig | y | | | | |
| storageResource | y | | | | |
| storageResourceCapabilityProfile | y | | | | |
| storageTier | y | | | | |
| systemCapacity | y | | | | |
| treeQuota | y | y | | | |
| userQuota | y | y | | | |
| virtualDisk | y | | | | |
| virtualVolume | y | | | | |
| dae | y | | | | |
| disk | y | | | | |
| dpe | y | | | | |
| encryption | y | | | | |
| ethernetPort | y | | | | |
| kmipServer | y | y | | | |
| ssc | y | | | | |
| ssd | y | | | | |
| storageProcessor | y | | | | |
| autodownloadSoftwareVersion | y | | | | |
| basicSystemInfo | y | | | | |
| candidateSoftwareVersion | y | | | | |
| feature | y | | | | |
| importSession | y | | | | |
| installedSoftwareVersion | y | | | | |
| license | y | | | | |
| ntpServer | y | | | | |
| remoteSyslog | y | y | | | |
| serviceContract | y | | | | |
| softwareUpgradeSession | y | | | | |
| system | y | | | | |
| systemInformation | y | | | | |
| systemLimit | y | | | | |
| systemTime | y | | | | |
| tbn | y | | | | |
| tbnConfig | y | | | | |
| upgradeSession | y | | | | |
| archive | y | | | | | 
| metric | | | | | | 
| metricCollection | | | | | | 
| metricQueryResult | | | | | | 
| metricRealTimeQuery | | | | | | 
| metricService | | | | | | 
| metricValue | | | | | | 
| ldapServer | y | y | | | |
| remoteInterface | y | | | | |
| replicationInterface | y | y | | | |
| replicationSession | y | y | | | |
| snap | y | y | | | |
| snapSchedule | y | y | | | |
| ioLimitPolicy | y | | | | |
| ioLimitRule | y | | | | |
| ioLimitSetting | y | | | | |
| configCaptureResult | | | | | |
| coreDump | | | | | |
| dataCollectionResult | | | | | |
| esrsParam | y | | | | |
| esrsPolicyManager | y | | | | |
| serviceAction | y | | | | |
| serviceInfo | y | | | | |
| supportAsset | y | | | | |
| supportProyy | y | | | | |
| supportService | y | | | | |
| technicalAdvisory | y | | | | |
| crl | y | | | | |
| loginSessionInfo | y | | | | |
| role | y | | | | |
| roleMapping | y | y | | | |
| securitySettings | y | | | | |
| user | y | y | | | |
| x509Certificate | y | | | | |
