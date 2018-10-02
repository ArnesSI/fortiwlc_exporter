import requests
import json
import sys
from pprint import pprint

ssidapi = [
    'https://wlc1.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
    'https://wlc6.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=g50dd0m861fw7zdh7HdQ391nrg5f41',
]
ssidclientapi = [
    'https://wlc1.anso.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
    'https://wlc6.anso.arnes.si/api/v2/monitor/wifi/client/select/?vdom=root&access_token=g50dd0m861fw7zdh7HdQ391nrg5f41',
]

#test source api
testing = ['https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7']

#production source api
production = [
    'https://wlc1.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
    'https://wlc6.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=g50dd0m861fw7zdh7HdQ391nrg5f41',
]

#ap_profile dictionaries
ap_profile_dict = {}
wlcprofiles = {}
data = None
datassid = None
#restructure the whole script
totalcamps = 0
totalaps = 0
totalwlccamps = 0
totalwlcaps = 0

maindict = {
    'ap': {}
}




def init():
    global ap_profile_dict, wlcprofiles, data, datassid, maindict
    ap_profile_dict = {}
    wlcprofiles = {}
    data = None
    datassid = None

    maindict = {
        'ap': {}
    }


def client_count(path,ap,perradio):
    clients = ap['clients']
    path['client_count'] += clients

    if ap['radio'][0]['mode'] == 'AP':
        radio1clients = ap['radio'][0]['client_count']

    if ap['radio'][1]['mode'] == 'AP':
        radio2clients = ap['radio'][1]['client_count']

    if perradio:
        path['per_radio']['1'] = radio1clients
        path['per_radio']['2'] = radio2clients


def wlc_hostname(z,wlcarray):
    wlc_name = ''
    if wlcarray == 'production':
        wlc_name = production[z]
    elif wlcarray == 'testing':
        wlc_name = testing[z]
    cutstring = ''
    cutstring = wlc_name.split('/')
    wlc_name = cutstring[2]
    return wlc_name


def ap_profile_string(ap):
    ap_profile = ap['ap_profile']
    cutstring = ''
    cutstring = ap_profile.split('_')
    campus = ''.join(cutstring[:-1])
    model = cutstring[-1]
    if model == 'FAP221E-default' or model == 'FAP223E-default':
        model = model[:-8]
    '''if campus == '':
        return model
    else:
        return [model, campus]'''
    return [model,campus,ap_profile]


def ap_write(ap,wlc_name):
    name = ap['name']
    maindict['ap'][name] = {
        'campus_name': '',
        'profile_name': '',
        'model': '',
        'wlc': '',
        'status': '',
        'state': '',
        'client_count': 0,
        'per_radio': {
            '1': 0,
            '2': 0
        },
        'ssid': {
            'ssid': '',
            'campus_id': '',
            'radious_group': ''
        }
    }
    appath = maindict['ap'][name]
    appath['campus_name'] = ap_profile_string(ap)[1]
    appath['profile_name'] = ap_profile_string(ap)[2]
    appath['model'] = ap_profile_string(ap)[0]
    appath['wlc'] = wlc_name
    appath['status'] = ap.get('status', None)
    appath['state'] = ap['state']
    client_count(appath,ap,True)


def ap_read_trough(wlc_name):
    for ap in data:
        ap_write(ap,wlc_name)


def main(ssidapi,wlcarray):
    global data, datassid
    init()
    z = 0
    if wlcarray == 'production':
        for wlc in production:
            wlc_hostname(z,wlcarray)
            '''ssidclienturl = ssidclientapi[z]
            ssidclientrresponse = requests.get(ssidclienturl)
            datassid = (ssidresponse.json()['results'])'''

            '''ssidcurl = ssidapi[z]
            ssidresponse = requests.get(ssidurl)
            datassid = (ssidresponse.json()['results'])'''

            url = production[z]
            response = requests.get(url)
            data = (response.json()['results'])
            ap_read_trough(wlc_hostname(z,wlcarray))
            z += 1
        return maindict

    elif wlcarray == 'testing':
        for wlc in testing:
            wlc_hostname(z,wlcarray)
            '''ssidclienturl = ssidclientapi[z]
            ssidclientrresponse = requests.get(ssidclienturl)
            datassid = (ssidresponse.json()['results'])'''

            '''ssidcurl = ssidapi[z]
            ssidresponse = requests.get(ssidurl)
            datassid = (ssidresponse.json()['results'])'''

            url = testing[z]
            response = requests.get(url)
            data = (response.json()['results'])
            ap_read_trough(wlc_hostname(z,wlcarray))
            z += 1
        return maindict


if __name__ == "__main__":
    wlcarray = sys.argv[1]
    print(json.dumps(main(ssidapi,wlcarray), indent = 4, sort_keys = False))
