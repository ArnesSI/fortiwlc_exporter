import requests


class FortiWLC:
    """ Class that collects WIFI data from FortiNET API """

    MANAGED_AP_URL = 'https://{name}/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token={api_key}'  # noqa
    VAP_GROUP_URL = 'https://{name}/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token={api_key}'  # noqa
    CLIENT_URL = 'https://{name}/api/v2/monitor/wifi/client/select/?vdom=root&access_token={api_key}'  # noqa

    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.clear()

    def clear(self):
        self.managed_ap = None
        self.vap_group = None
        self.clients = None

    def _get(self, url):
        resp = requests.get(url)
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
