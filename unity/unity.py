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
        print(response.url)
        return response.json()

    def _delete_instance(self, resource, rid, payload=None):
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        response = self.session.delete(endpoint, params=payload)
        return response.json()

    def _create_instance(self, resource, payload=None):
        if not payload:
            return
        else:
            body = json.dumps(payload)
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
            response = self.session.post(endpoint, data=body)
            return response.json()

    def get_resource(self, resource, name=None, rid=None, **kwargs):
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
        res = resource
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    # Configuring network communication
    def get_cifsServer(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'cifsServer'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_dnsServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'dnsServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileDNSServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileDNSServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileInterface(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileInterface'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileKerberosServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileKerberosServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileLDAPServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileLDAPServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileNISServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileNISServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fsnPort(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fsnPort'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_ftpServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'ftpServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_ipInterface(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'ipInterface'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_ipPort(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'ipPort'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_iscsiNode(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'iscsiNode'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_iscsiPortal(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'iscsiPortal'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_iscsiSettings(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'iscsiSettings'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_linkAggregation(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'linkAggregation'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_mgmtInterface(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'mgmtInterface'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_mgmtInterfaceSettings(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'mgmtInterfaceSettings'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_nasServer(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'nasServer'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

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

    def get_nfsServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'nfsServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_preferredInterfaceSettings(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'preferredInterfaceSettings'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_route(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'route'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_smtpServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'smtpServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_tenant(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'tenant'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_urServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'urServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_virusChecker(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'virusChecker'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_vlanInfo(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'vlanInfo'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_vmwareNasPEServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'vmwareNasPEServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    ## Managing events and alerts

    def get_alert(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'alert'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_alertConfig(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'alertConfig'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_alertConfigSNMPTarget(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'alertConfigSNMPTarget'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_alertEmailConfig(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'alertEmailConfig'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_event(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'event'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    ## Managing jobs

    def get_job(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'job'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    ## Managing remote systems

    def get_cifsShare(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'cifsShare'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_datastore(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'datastore'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_host(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'host'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_hostContainer(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'hostContainer'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_hostIPPort(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'hostIPPort'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_hostInitiator(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'hostInitiator'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_hostInitiatorPath(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'hostInitiatorPath'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_hostLun(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'hostLun'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_hostVVolDatastore(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'hostVVolDatastore'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_nfsShare(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'nfsShare'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_remoteSystem(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'remoteSystem'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_rpChapSettings(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'rpChapSettings'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_vm(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'vm'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_vmDisk(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'vmDisk'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_vmwarePE(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'vmwarePE'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    ## Managing storage

    def get_aclUser(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'aclUser'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_capabilityProfile(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'capabilityProfile'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_dhsmConnection(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'dhsmConnection'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_dhsmServer(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'dhsmServer'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fastCache(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fastCache'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fastVP(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fastVP'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileEventsPool(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileEventsPool'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_fileEventsPublisher(self, rid=None, **kwargs):
        """
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'fileEventsPublisher'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_filesystem(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'filesystem'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_lun(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'lun'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_moveSession(self, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'moveSession'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_pool(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'pool'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_poolConsumer(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'poolConsumer'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_poolConsumerAllocation(self, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'poolConsumerAllocation'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_poolUnit(self, name=None, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'poolUnit'
        if name and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            return self._get_instance(res, rname=name, payload=kwargs)
        elif rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)

    def get_quotaConfig(self, rid=None, **kwargs):
        """
        :param name: Name of the resource to query (optional)
        :param rid: Resource ID (internal ID) of the resource to query (optional)
        :param kwargs: Additional accepted keyword arguments to modify the query:
                        fields:  Comma separated list of fields to return
                        filter:  Filter for the query
                        groupby:  Group the results by a property
                        compact:  If true, metadata is ignored (instance queries only)
        :return: A query by name, id, or the entire collection will return
                    the object's ID, if no other fields are specified.  If
                    other fields are specified, and they are available via
                    this resource, they will be returned as well
        """
        res = 'quotaConfig'
        if rid:
            return self._get_instance(res, rid=rid, payload=kwargs)
        else:
            return self._get_collection(res, payload=kwargs)
    ## Managing the environment
    ## Managing the system
    ## Monitoring capacity and performance
    ## Protecting data
    ## Quality Of Service
    ## Servicing the system
    ## User and security