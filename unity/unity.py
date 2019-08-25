from unity import classes
import json
import requests


class Unity(object):
    """
    Initializes the object.

    Design:

    All methods defined in this class will follow a specific pattern:

    _function_name - This is an internal function, not meant to be used directly


    Function Arguments:

    All required arguments for the function will be positional (and therefore
    required).  All optional arguments will be named (**kwargs).  The only exception
    is optional arguments that require a dictionary:

        myArgument={'id': 'myId'}

    @todo Need to add some unittests for all the methods
    """
    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password
        self.session = None

    def __getattr__(self, attr):
        """
        This is a handy little function that can be used as a discovery
        mechanism.  It allows easy exploration of the objects in the
        Unity REST API.  This is designed to be used interactively.  Use
        the specific functions for the resource you're working with for
        real work.

        Example:
            Instantiate the object:

                > unity = unity('hostname', user, password)

            Login to the API:

                > unity.connect()

            View the 'filesystem' resource from the API:

                > unity.filesystem

        This function does have a weakness currently.  The Unity REST API
        only returns the ID attribute by default, unless the GET request
        specifies more properties.  This function would be more useful if
        all properties were returned for each resource.

        @todo -> Come up with a way to return all properties of each object
                explored with this function
        """
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            if self.session is None:
                print('Not connected.')
            else:
                return Unity._get_collection(self, attr)

    def connect(self):
        """
        Method to connect to the Unity REST API.

        Examples:
            > unity.connect()


        :returns
            If the connection is successful, it will set the 'session' property
            of the Unity object to the requests.session object we used to login
            so we can use the same session for all subsequent operations.
        """
        if self.session is not None:
            print('A session already exists for this object')
            return
        else:
            headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-EMC-REST-CLIENT': 'true'
            }
            requests.packages.urllib3.disable_warnings()
            login_uri = 'https://{}/{}/{}'.format(self.name, 'api/types', 'system/instances')
            session = requests.Session()
            session.headers.update(headers)
            session.auth = (self.user, self.password)
            login = session.get(login_uri, verify=False)
            # print(login.json())
            token = login.headers.get('EMC-CSRF-TOKEN')
            session.headers.update({'EMC-CSRF-TOKEN': token})
            self.session = session

    def disconnect(self):
        """
        Method to logout of the Unity REST API.

        Examples:
            > unity.disconnect()

        Attributes:
            No attributes for this method.  All attributes required to execute
            the connection are defined during the object creation and
            connect methods.

        """
        if type(self.session) is requests.sessions.Session:
            logout_uri = 'https://%s/api/types/loginSessionInfo/action/logout' % self.name
            self.session.post(logout_uri, verify=False)
            # Reset the session to None after logout occurs.
            self.session = None
        else:
            print('There is no active session to disconnect for this object')
            return

    def jsonify(self, data):
        json_data = json.dumps(data.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data

    def _get_collection(self,  resource, payload=None):
        """
        Internal function for collection queries
        @todo -> need to add a decorator to process HTTP responses
        :param resource:
        :param payload:
        :return:
        """
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
        response = self.session.get(endpoint, params=payload)
        return response.json()

    def _get_instance(self, resource, rname=None, rid=None, payload=None):
        payload = payload or {'compact': 'true'}
        if rid:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        elif rname:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(rname))
        else:
            return
        response = self.session.get(endpoint, params=payload)
        return response.json()

    def _delete_instance(self, resource, rid, payload=None):
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        response = self.session.delete(endpoint, params=payload)
        return response.json()

    def new(self, resource, payload=None):
        """
        @todo need to support async requests
        :param resource:
        :param payload:
        :return:
        """
        if not payload:
            return
        else:
            body = self.jsonify(payload)
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
            response = self.session.post(endpoint, data=body)
            return response.json()

    def _modify_instance(self, resource, rname=None, rid=None, payload=None):
        """
        @todo  Need to support async requests.
        :param resource:
        :param rname:
        :param rid:
        :param payload:
        :return:
        """
        if rid:
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid, 'action/modify')
        elif rname:
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(rname),
                                                       'action/modify')
        else:
            return
        response = self.session.post(endpoint, params=payload)
        print(response.url)
        return response.json()

    def _instance_action(self, resource, action, payload=None):
        if not payload:
            return
        else:
            #body = json.dumps(payload)
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'action', action)
            response = self.session.post(endpoint, data=payload)
            return response.json()

    def get(self, resource, name=None, id=None, **kwargs):
        """
        One query function to rule them all.

        We can use this to query any instance or collection in the system.
        This first positional parameter is the resource we're querying.
        Function can query by name or ID.  If no name or ID is specified,
        then the collection is queried.

        For a list of resources to query, look at the API documentation:

        https://<UNITY_HOSTNAME>/apidocs/index.html

        :param resource:  Type of the resource to query
        :param name: Name of the resource to query (optional)
        :param rid: Internal ID (rid = Resource ID) to query (optional)
        :param kwargs: Additional keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned.
        """
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(resource, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(resource, rid=rid, payload=kwargs)
        else:
            return self._get_collection(resource, payload=kwargs)

    #def new(self, resource, payload=None):


    # Resource-specific functions

    def new_nasServer(self, name, homeSP, poolId, tenantId=None, **kwargs):
        """
        :param name: Name of the NAS Server to create
        :param homeSP: ID of the SP (spa, spb) to create the NAS Server on
        :param poolId: ID of the storage pool to create the NAS Server in
        :param tenantId:  ID of the tenant to create the NAS Server in.  This
                        argument is optional, but requires a dictionary.

                        This enables you to specify the tenant ID like this:

                        u.new_nasServer(name, homeSP, poolId, tenantId=<id>)

                        Instead of this:

                        u.new_nasServer(name, homeSP, poolId, tenant={'id': <id>})
        :param kwargs: All additional parameters are named, and optional.
                        Review the API documentation for information on the
                        additional properties accepted.
        :return: ID of the NAS Server that is created:

                    content': {u'id': u'nas_3'}
        """
        res = 'nasServer'
        data = {
            'name': name,
            'homeSP': {
                'id': homeSP
            },
            'pool': {
                'id': poolId
            }
        }
        if tenantId is not None:
            tenant = {
                'tenant': {
                    'id': tenantId
                }
            }
            data.update(tenant)
        if kwargs:
            data.update(kwargs)
        return self._create_instance(res, payload=data)

    def new_filesystem(self, name, nasServer, size, poolId, **kwargs):
        """
        :param name: Name of the filesystem to create
        :param nasServer: Name of the NAS Server to create the filesystem on
        :param size: Size of the filesystem.
                    Specify size in gigabytes like so:  100G or 100.2G
                        Not sure why you'd specify a float here, but you do you
                    Specify size in terabytes like so:  1T or 1.2T

                    Floating points will work, but will be converted to bytes
                    and rounded down.

        :param poolId: ID of the storage pool to create the filesystem on
        :param kwargs: All other optional parameters
        :return: ID of the filesystem created
        """
        res = 'storageResource'
        act = 'createFilesystem'
        fs = classes.StorageResourceFilesystem(name, poolId, nasServer, size, **kwargs)
        data = fs.jsonify()
        print(data)
        return self._instance_action(res, act, payload=data)

    def new_fileDNSServer(self, nasServer, domain, addresses, **kwargs):
        """
        :param nasServer: ID of the NAS Server to configure DNS
        :param domain: Name of the domain
        :param addresses: Address list (prioritized)
        :return: ID of the fileDNSServer instance
        @todo need to test this function
        """
        res = 'fileDNSServer'
        address_list = addresses.split(',')
        data = {
            'nasServer': {
                'id': nasServer
            },
            'domain': domain,
            'addresses': address_list
        }
        if kwargs:
            data.update(kwargs)
        return self._create_instance(res, payload=data)

    def new_fileInterface(self, nasServer, ipPort, ipAddress, netmask, gateway, **kwargs):
        """
        :param nasServer: ID of the NAS Server to create the interface on
        :param ipPort: The ethernet port on which to create the interface
        :param ipAddress: IP address of the interface
        :param netmask: Netmask for the interface
        :param gateway: Default gateway of the interface
        :return: ID of the interface created
        """
        res = 'fileInterface'
        data = {
            'nasServer': {
                'id': nasServer
            },
            'ipPort': {
                'id': ipPort
            },
            'ipAddress': ipAddress,
            'netmask': netmask,
            'gateway': gateway
        }
        if kwargs:
            data.update(kwargs)
        return self._create_instance(res, payload=data)

