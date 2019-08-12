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

`> vsa.get_filesystem()`

### Query an instance by name (filesystem)

`> vsa.get_filesystem(name='myFilesystem')`

### Query an instance by ID (filesystem)

`> vsa.get_filesystem(rid='fs_1')`

### Query an instance with field specifications and query modifiers (filesystem)

`> vsa.get_filesystem(name='myFilesystem', fields='id,name,sizeUsed', compact='true')`
