import requests


class Unity(object):
    """
    Initializes the object.
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
        Unity REST API.

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

        @todo -> Come up with a way to return al properties of each object
                explored with this function
        """
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            if self.session is None:
                print('Not connected.')
            else:
                return Unity.get_collection(self, attr)

    def connect(self):
        """
        Method to connect to the Unity REST API.

        Examples:
            > unity.connect()

        Todo:
            - Should we return the results of the GET that we use to login
                (the system collection)?
            - We need to add some code to process the HTTP response

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
            print(login_uri)
            session = requests.Session()
            session.headers.update(headers)
            session.auth = (self.user, self.password)
            login = session.get(login_uri, verify=False)
            print(login.text)
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

        Todo:
        """
        if type(self.session) is requests.sessions.Session:
            logout_uri = 'https://%s/api/types/loginSessionInfo/action/logout' % self.name
            self.session.post(logout_uri, verify=False)
            # Reset the session to None after logout occurs.
            self.session = None
        else:
            print('There is no active session to disconnect for this object')
            return

    def get_collection(self,  resource, payload=None):
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/types', resource, 'instances')
        response = self.session.get(endpoint, params=payload)
        return response.json()

    def get_instance(self, resource, rid, payload=None):
        payload = payload or {'compact': 'true'}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        response = self.session.get(endpoint, params=payload)
        return response.json()

    def delete_instance(self, resource, rid, payload=None):
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(self.name, 'api/instances', resource, rid)
        response = self.session.delete(endpoint, params=payload)
        return response.json()

    def
