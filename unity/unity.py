import json
import requests
from unity import classes


class Unity:

    def __init__(self, name, user, password):
        """
        Object instantiation.
        :param name: This is the name or IP of the Unity
        :param user: Username to log in with
        :param password: Password to log in with

        There are some other properties that I'm setting as empty for now.
        They will be used to for sub-classes (not inherited) after the
        connect() method is executed.  In those sub-classes will be functions
        specific to the resource.

        """
        self.name = name
        self.user = user
        self.password = password
        self.session = None
        self.storageResource = None

    def __getattr__(self, attr):
        """
        This is a handy little function that can be used as a discovery
        mechanism.  It allows easy exploration of the objects in the
        Unity REST API.  This is designed to be used interactively.  Use
        the 'get' function for real work.

        Example:
            Instantiate the object:

                > unity = Unity('hostname', user, password)

            Login to the API:

                > unity.connect()

            View the 'filesystem' resource from the API:

                > unity.filesystem

        This function does have a weakness currently.  The Unity REST API
        only returns the ID attribute by default, unless the GET request
        specifies more properties.  This function would be more useful if
        all properties were returned for each resource.
        """
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            if self.session is None:
                print('Not connected.  You must execute connect() first.')
            else:
                return Unity.get(self, attr)

    def connect(self, quiet: bool = False):
        """
        Method to connect to the Unity REST API.

        Examples:

            > unity.connect()

        This will return the following properties from the query we have
        to use to log in:

        Name
        Platform
        Model
        Serial Number

        If the 'quiet' parameter is set to 'true', the connect method will
        not return anything (might be useful in a script).
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
            login_uri = 'https://{}/{}'.format(self.name, 'api/instances/system/0')
            session = requests.Session()
            session.headers.update(headers)
            session.auth = (self.user, self.password)
            parameters = {
                'compact': 'true',
                'fields': 'name,platform,model,serialNumber'
            }
            login = session.get(login_uri, verify=False, params=parameters)
            token = login.headers.get('EMC-CSRF-TOKEN')
            session.headers.update({'EMC-CSRF-TOKEN': token})
            self.session = session
            self.storageResource = storageResource(self.name, self.session)
            if quiet is False:
                return login.json()

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
            logout_uri = 'https://{}/api/types/loginSessionInfo/action/logout'.format(self.name)
            self.session.post(logout_uri, verify=False)
            self.session = None
            self.storageResource = None
        else:
            print('There is no active session to disconnect for this object')
            return

    @staticmethod
    def jsonify(data):
        json_data = json.dumps(data.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data

    def delete(self, resource, rname=None, rid=None, timeout=None, **kwargs):
        """

        :param resource: Type of resource to delete.  Must match the name (and case)
                        of the resource in the API
        :param rname: "Resource Name".  Name of the resource to delete.
        :param rid: "Resource ID".  ID of the resource to delete
        :param timeout: Operation timeout.  For asynchronous requests (set to 0)
        :param kwargs:  Some delete operations take some additional options
                        like forcefully deleting snaps when deleting a storage resource.
        :return: Response code 204/202 (async)
        """
        if rname and id:
            print('You cannot specify a name and an ID.')
            return
        elif rname:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(rname))
        elif rid:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        else:
            print('No instance to given to delete.')
            return
        timeout = timeout or {}
        body = json.dumps(kwargs)
        response = self.session.delete(endpoint, params=timeout, data=body)
        return response

    def create(self, resource, *args, timeout=None, **kwargs):
        """
        This function converts a python object to json and posts it to the
        right endpoint.  This function will work only if a class for the resource
        is defined in the classes.py file.  It will look up the required class
        and instantiate it with the arguments (from *args and **kwargs).
        @todo need to support async requests
        :param resource: name of the resource to create
        :param timeout: timeout value.  Set to 0 for asynchronous requests
        :return: ID of the resource created, if successful
        """
        class_name = getattr(classes, resource)
        if not class_name:
            print('Invalid resource name or class does not exist.')
        obj = class_name(*args, **kwargs)
        body = Unity.jsonify(obj)
        timeout = timeout or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
        response = self.session.post(endpoint, data=body, params=timeout)
        return response.json()

    def modify(self, resource, rname=None, rid=None, timeout=None, **kwargs):
        """
        :param resource:
        :param rname:
        :param rid:
        :param timeout:
        :return:
        """
        if rid:
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid, 'action/modify')
        elif rname:
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(rname),
                                                       'action/modify')
        else:
            print('No resource name or ID specified.')
            return
        timeout = timeout or {}
        body = json.dumps(kwargs)
        response = self.session.post(endpoint, params=timeout, data=body)
        return response

    def get(self, resource, rname=None, rid=None, **kwargs):
        """
        One query function to rule them all.

        We can use this to query any instance or collection in the system.
        This first positional parameter is the resource we're querying.
        Function can query by name or ID.  If no name or ID is specified,
        then the collection is queried.

        For a list of resources to query, look at the API documentation:

        https://<UNITY_HOSTNAME>/apidocs/index.html

        :param rname:
        :param rid:
        :param resource:  Type of the resource to query
        :param name: Name of the resource to query (optional)
        :param id: Internal ID (rid = Resource ID) to query (optional)
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
        if rname and rid:
            print('You cannot specify both a name and an ID.')
            return
        elif rname:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(rname))
        elif rid:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        else:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
        response = self.session.get(endpoint, params=kwargs)
        return response.json()

    def download(self, nasServerId: str, fileType: int):
        """
        :param nasServerId: NAS Server to download configuration file from
        :param fileType: Type of configuration to download:
                1 - Ldap_Configuration (LDAP schema file)
                2 - Ldap_CA_Certificate
                3 - Username_Mappings
                4 - Virus_Checker_Configuration
                5 - Users
                6 – Groups
                7 - Hosts
                8 - Netgroups
                9 - User_Mapping_Report
                10 - Kerberos_Key_Table
                11 - Homedir
        :return: raw file in response body
        """
        endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'download', fileType, 'nasServer', nasServerId)
        print(endpoint)
        response = self.session.get(endpoint, stream=True)
        return response.content

    def upload(self, nasServerId: str, fileType: int, filePath: str):
        """
        :param nasServerId: ID of the NAS Server to upload to
        :param fileType: Type of configuration file to upload
                1 - Ldap_Configuration (LDAP schema file)
                2 - Ldap_CA_Certificate
                3 - Username_Mappings
                4 - Virus_Checker_Configuration
                5 - Users
                6 – Groups
                7 - Hosts
                8 - Netgroups
                9 - User_Mapping_Report
                10 - Kerberos_Key_Table
                11 - Homedir
        :param filePath: Path to the file to upload.  Will be read as binary
                        and posted to the specified fileType location
        :return: Response 200/204 for success
        """
        endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'upload', fileType, 'nasServer', nasServerId)
        file = {'file': open(filePath, "rb")}
        del self.session.headers['Content-Type']
        response = self.session.post(endpoint, files=file)
        self.session.headers.update({'Content-Type': 'application/json'})
        return response


class storageResource:
    def __init__(self, name, session):
        self.name = name
        self.session = session

    @staticmethod
    def jsonify(data):
        json_data = json.dumps(data.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data

    def get(self, rid=None, rname=None, **kwargs):
        if rname and rid:
            print('You cannot specify a name and an ID.')
            return
        elif rid:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', rid)
        elif rname:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', 'name:{}'.format(rname))
        else:
            endpoint = 'https://{}/{}'.format(self.name, 'api/types/storageResource/instances')
        response = self.session.get(endpoint, params=kwargs)
        return response.json()

    def create(self, resource, *args, timeout=None, **kwargs):
        """

        :param timeout:
        :param resource:
        :param payload:
        :return:
        """
        action = 'create{}'.format(resource)
        class_name = getattr(classes, resource)
        if not class_name:
            print('Invalid resource name or class does not exist.')
            return
        obj = class_name(*args, **kwargs)
        endpoint = 'https://{}/{}/{}'.format(self.name, 'api/types/storageResource/action', action)
        body = Unity.jsonify(obj)
        timeout = timeout or {}
        response = self.session.post(endpoint, params=timeout, data=body)
        return response.json()

    def delete(self, rid=None, rname=None, timeout=None, **kwargs):
        if rname and rid:
            print('Cannot specify a name and an ID.')
            return
        elif rname:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', 'name:{}'.format(rname))
        elif rid:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', rid)
        else:
            print('No resource specified.')
            return
        body = json.dumps(kwargs)
        response = self.session.delete(endpoint, params=timeout, data=body)
        return response

    def modify(self, resource, rid=None, rname=None, timeout=None, **kwargs):
        """
        @todo - need to complete and test.
        :param resource:
        :param rid:
        :param rname:
        :param timeout:
        :param kwargs:
        :return:
        """
        if rid:
            action = 'Modify{}'.format(resource)
        elif rname:
            action = 'Modify{}ByName'.format(resource)
        else:
            print('You must provide a name or ID of a {} to modify'.format(resource))
            return
        class_name = getattr(classes, resource)
        if not class_name:
            print('Invalid resource or class does not exist.')
            return
        obj = class_name(*kwargs)
        endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances/storageResource/', rid, 'action', action )
