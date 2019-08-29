# emcpy
Python Client for EMC NAS (Unity/VNX) Platforms

## Unity

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