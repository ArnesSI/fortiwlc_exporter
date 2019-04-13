import requests

from .utils import timeit


class FortiWLC:
    """ Class that collects WIFI data from FortiNET API """

    LOGIN_URL = 'https://{name}/logincheck'
    LOGOUT_URL = 'https://{name}/logout'
    MANAGED_AP_URL = 'https://{name}/api/v2/monitor/wifi/managed_ap/select/?vdom=root'
    VAP_GROUP_URL = (
        'https://{name}/api/v2/cmdb/wireless-controller/vap-group/?vdom=root'
    )
    CLIENT_URL = 'https://{name}/api/v2/monitor/wifi/client/select/?vdom=root'

    def __init__(self, name, api_key=None, username=None, password=None):
        self.name = name
        self.api_key = api_key
        self.username = username
        self.password = password
        self.last_pool_ok = False
        self.clear()
        self._session = None

    def clear(self):
        self.last_pool_ok = False
        self.managed_ap = []
        self.vap_group = []
        self.clients = []

    def _login(self, force=False):
        ''' Login and store session data if not using API keys '''
        if self._session and not force:
            return
        if self.api_key:
            self._session = requests.session()
            self._session.headers['Authorization'] = 'Bearer {}'.format(self.api_key)
        else:
            session = requests.session()
            login_url = self.LOGIN_URL.format(name=self.name)
            params = {"username": self.username, "secretkey": self.password, "ajax": 1}
            response = session.post(login_url, params=params)
            if not response.ok or str(response.text)[0] != '1':
                raise AttributeError("Denied access: %s" % response)
            self._session = session

    def logout(self):
        if not self.api_key:
            url = self.LOGOUT_URL.format(name=self.name)
            self._session.post(url)
        self._session = None

    def _get(self, url):
        self._login()
        resp = self._session.get(url)
        resp.raise_for_status()
        return resp.json()

    @timeit
    def get_managed_ap(self):
        """ Returns info about APs (access points) """
        url = self.MANAGED_AP_URL.format(name=self.name, api_key=self.api_key)
        return self._get(url)

    @timeit
    def get_vap_group(self):
        """ Returns info about configured VAPs (SSIDs) """
        url = self.VAP_GROUP_URL.format(name=self.name, api_key=self.api_key)
        return self._get(url)

    @timeit
    def get_clients(self):
        """ Returns info about connected WIFI clients """
        url = self.CLIENT_URL.format(name=self.name, api_key=self.api_key)
        return self._get(url)

    def poll(self):
        try:
            self.clear()
            self.managed_ap = self.get_managed_ap()['results']
            self.vap_group = self.get_vap_group()['results']
            self.clients = self.get_clients()['results']
            self.logout()
        except Exception:
            # TODO log error
            self.last_pool_ok = False
        else:
            self.last_pool_ok = True
