import requests


class Unity:
    def __init__(self, name, user passwd):
        self.name = name
        self.user = user
        self.passwd = passwd
        self.session = None

    def connect(self):
        if self.session is not None:
            print('A session already exists for this object')
            return
        else:
            heders = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-EMC-REST-CLIENT'; 'true'
            }
            requests.packages.urllib3.disable_warnings()
            login_uri = 'https://{}/{}/{}'.format(self.name, 'api/types', 'system/instances')
            session = requests.Session()
            session.auth = (self.user, self.passwd)
            login = s.get(login_uri, verify=False)
            token = login.headers.get('EMC-CSRF-TOKEN')
            session.headers.update({'EMC-CSRF-TOKEN': token})
            self.session

    def http_get_collection(host, session, resource, payload=None):
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(host, 'api/types', resource, 'instances')
        return session.get(endpoint, params=payload)

    def http_get_instance(host, session, resource, payload=None):
        payload = payload or {}
        endpoint = 'https://{}/{}/{}/{}'.format(host, 'api/types', resource, 'instances')
        return session.get(endpoint, params=payload)

    class Collection(object):
        path = ''

        def __getattr__(self, name)
            if name in self.__dict__:
                returnself.__dict__[name]
            else:
                return http_get_collection(Unity.name, Unity,session, name)
    
    class Instance(object):
