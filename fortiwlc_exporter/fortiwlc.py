import requests


class FortiWLC:
    """ Class that collects WIFI data from FortiNET API """

    LOGIN_URL = 'https://{name}/logincheck'
    LOGOUT_URL = 'https://{name}/logout'
    MANAGED_AP_URL = 'https://{name}/api/v2/monitor/wifi/managed_ap/select/?vdom=root'  # noqa
    VAP_GROUP_URL = 'https://{name}/api/v2/cmdb/wireless-controller/vap-group/?vdom=root'  # noqa
    CLIENT_URL = 'https://{name}/api/v2/monitor/wifi/client/select/?vdom=root'  # noqa

    def __init__(self, name, api_key=None, username=None, password=None):
        self.name = name
        self.api_key = api_key
        self.username = username
        self.password = password
        self.clear()
        self._session = None

    def clear(self):
        self.managed_ap = None
        self.vap_group = None
        self.clients = None

    def _login(self, force=False):
        ''' Login and store session data if not using API keys '''
        if self.api_key and (force or not self._session):
            self._session = requests.session()
            self._session.headers['Authorization'] = 'Bearer {}'.format(self.api_key)
        elif not self.api_key and (force or not self._session):
            self._session = requests.session()
            login_url = self.LOGIN_URL.format(self.name)
            params = {
                "username": self.username,
                "secretkey": self.password,
                "ajax": 1,
            }
            response = self._session.post(login_url, params=params)
            if not response.ok:
                raise AttributeError("Denied access: %s" % response)

    def logout(self):
        if not self.api_key:
            url = self.LOGOUT_URL.format(self.name)
            self._session.post(url)
        self._session = None

    def _get(self, url):
        self._login()
        resp = self._session.get(url)
        resp.raise_for_status()
        return resp.json()['results']

    def get_managed_ap(self):
        """ Returns info about APs (access points) """
        url = self.MANAGED_AP_URL.format(name=self.name, api_key=self.api_key)
        return self._get(url)

    def get_vap_group(self):
        """ Returns info about configured VAPs (SSIDs) """
        url = self.VAP_GROUP_URL.format(name=self.name, api_key=self.api_key)
        return self._get(url)

    def get_clients(self):
        """ Returns info about connected WIFI clients """
        url = self.CLIENT_URL.format(name=self.name, api_key=self.api_key)
        return self._get(url)

    def poll(self):
        self.clear()
        self.managed_ap = self.get_managed_ap()
        self.vap_group = self.get_vap_group()
        self.clients = self.get_clients()
        self.logout()
