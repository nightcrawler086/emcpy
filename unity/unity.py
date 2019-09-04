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

    def connect(self, quiet: bool = 'false'):
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
            if quiet == 'false':
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
            logout_uri = 'https://%s/api/types/loginSessionInfo/action/logout' % self.name
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

    """
    @staticmethod
    def json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())

    @staticmethod
    def json2obj(data):
        return json.loads(data, object_hook=Unity.json_object_hook)
    """

    def delete(self, resource, name=None, id=None, timeout=None, **kwargs):
        """

        :param resource:
        :param name:
        :param id:
        :param timeout:
        :param kwargs:
        :return:
        """
        if name and id:
            print('You cannot specify a name and an ID.')
            return
        elif name:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(name))
        elif id:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, id)
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
        print(args)
        obj = class_name(*args, **kwargs)
        body = Unity.jsonify(obj)
        timeout = timeout or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
        response = self.session.post(endpoint, data=body, params=timeout)
        return response.json()

    def modify(self, resource, iname=None, id=None, timeout=None, **kwargs):
        """
        :param resource:
        :param iname:
        :param id:
        :param timeout:
        :return:
        """
        if id:
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances', resource, id, 'action/modify')
        elif iname:
            endpoint = 'https://{}/{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(iname),
                                                       'action/modify')
        else:
            return
        timeout = timeout or {}
        body = json.dumps(kwargs)
        response = self.session.post(endpoint, params=timeout, data=body)
        return response

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
        if name and id:
            print('You cannot specify both a name and an ID.')
            return
        elif name:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, 'name:{}'.format(name))
        elif id:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, id)
        else:
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
        response = self.session.get(endpoint, params=kwargs)
        return response.json()


class storageResource:
    def __init__(self, name, session):
        self.name = name
        self.session = session

    @staticmethod
    def jsonify(data):
        json_data = json.dumps(data.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data

    def get(self, id=None, name=None, **kwargs):
        if name and id:
            print('You cannot specify a name and an ID.')
            return
        elif id:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', id)
        elif name:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', 'name:{}'.format(name))
        else:
            endpoint = 'https://{}/{}'.format(self.name, 'api/types/storageResource/instances')
        response = self.session.get(endpoint, params=kwargs)
        return response.json()

    def create(self, resource, *args, timeout=None, **kwargs):
        """

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

    def delete(self, id=None, name=None, timeout=None, **kwargs):
        if name and id:
            print('Cannot specify a name and an ID.')
            return
        elif name:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', 'name:{}'.format(name))
        elif id:
            endpoint = 'https://{}/{}/{}'.format(self.name, 'api/instances/storageResource', id)
        else:
            print('No resource specified.')
            return
        body = json.dumps(kwargs)
        response = self.session.delete(endpoint, params=timeout, data=body)
        return response

    def modify(self, resource, id=None, name=None, timeout=None, **kwargs):
        """
        :param resource:
        :param id:
        :param name:
        :param payload:
        :return:
        """
        if name and id:
            print('You cannot specify a name and an ID.')
            return
        elif name:
            action = 'modify{}ByName'.format(resource)
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances/storageResource', 'name:{}'.format(name),
                                                    'action/{}'.format(action))
        elif id:
            action = 'modify{}'.format(resource)
            endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances/storageResource', id,
                                                    'action/{}'.format(action))
        else:
            print('No instance name or ID given')
            return
        body = json.dumps(kwargs)
        timeout = timeout or {}
        response = self.session.post(endpoint, data=body, params=timeout)
        return response
