import requests
import json
from pprint import pprint

ssidapi = [
    'https://wlc1.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/cmdb/wireless-controller/vap-group/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
]

#test source api
testapiarray = ['https://wlc.ansoext.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=r8g1y84z1q73x96s91gQq0pfGNd4x7']

#production source api
productionapiarray = [
    'https://wlc1.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=kQ0bg3jg6pfn19kr4GdgzGx41dmk9w',
    'https://wlc2.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=9dprpq3xs8bxwGs10w03N5N9bt6dpp',
    'https://wlc3.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=60dzxQ3wNb1GbjjshryQ000NwN3yyj',
    'https://wlc4.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=wGzjNw1pQg5snmxp6m1jphQ94n41mw',
    'https://wlc5.anso.arnes.si/api/v2/monitor/wifi/managed_ap/select/?vdom=root&access_token=3696nbbws84k3078fnpzz3sN740zdc',
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
    'total': {
        'ap_count': {
            'total': 0,
            'status': {
                'connected': 0,
                'disconnected': 0,
                'authorized': 0,
                'discovered': 0
                },
            'reboot_last_day': 0,
            'per_model': {}
        }, 'wlc_count': 0,
        'campus_count': 0,
        'profile_count': 0,
        'client_count': 0,
        'ssid_count': 0,
        'ssids': set()
    },
    'wlc': {},
    'campus': {},
    'ap': {}
}


def init():
    global ap_profile_dict, wlcprofiles, data, datassid, maindict
    ap_profile_dict = {}
    wlcprofiles = {}
    data = None
    datassid = None

    maindict = {
        'total': {
            'ap_count': {
                'total': 0,
                'status': {
                    'connected': 0,
                    'disconnected': 0,
                    'authorized': 0,
                    'discovered': 0
                    },
                'reboot_last_day': 0,
                'per_model': {}
            }, 'wlc_count': 0,
            'campus_count': 0,
            'profile_count': 0,
            'client_count': 0,
            'ssid_count': 0,
            'ssids': set()
        },
        'wlc': {},
        'campus': {},
        'ap': {}
    }


def get_ssids_from_group(group,ssidset,path):
    for ssidgroup in datassid:
        if ssidgroup['name'] == group:
            for ssid in ssidgroup['vaps']:
                ssidset.add(ssid['name'])
                path['ssids'].add(ssid['name'])
    return ssidset


def ssid_count(path,ap):
    #print(ap['name'])
    ssidset = set()
    ssidset.clear()

    for ssidindex in ap['ssid']:
        for listindex in ssidindex['list']:
            if 'SGR_' in listindex:
                get_ssids_from_group(listindex,ssidset,path)
            else:
                ssidset.add(str(listindex))
    #print(ssidset)
    path['ssids'].update(ssidset)
    path['ssid_count'] = len(path['ssids'])


def ap_campus_counter(z):
    zstring = str(z)
    for ap in data:
        campus = ap_profile_string(ap)[1]
        camp = maindict['campus']
        if campus != '':
            if campus not in maindict['campus']:
                camp[campus] = {
                    'ap_count': {
                        'total': 0,
                        'status': {
                            'connected': 0,
                            'disconnected': 0,
                            'authorized': 0,
                            'discovered': 0
                        },
                        'reboot_last_day': 0,
                        'per_model': {}
                    },
                    'profile_count': 0,
                    'client_count': 0,
                    'ssid_count': 0,
                    'ssids': set()
                }
                maindict['wlc']['wlc'+zstring]['campus_count'] += 1
            camp[campus]['ap_count']['total'] += 1
            status_write(camp[campus]['ap_count']['status'],ap)
            reboot_last_day_write(camp[campus]['ap_count'],ap)
            per_model_write(camp[campus]['ap_count']['per_model'],ap,True)
            ap_profile_count(camp[campus],ap)
            client_count(camp[campus],ap,False)
            ssid_count(camp[campus],ap)
        else:
            path = maindict['wlc']['wlc'+zstring]['ap_count']
            path['total'] += 1
            per_model_write(path['per_model'],ap,False)
            status_write(path['status'],ap)
            reboot_last_day_write(path,ap)


def wlc_create(z):
    zstring = str(z)
    maindict['wlc']['wlc'+zstring] = {
        'ap_count': {
            'total': 0,
            'status': {
                'connected': 0,
                'disconnected': 0,
                'authorized': 0,
                'discovered': 0
                },
            'reboot_last_day': 0,
            'per_model':{}
            },
        'campus_count': 0,
        'profile_count': 0,
        'client_count': 0,
        'ssid_count': 0,
        'ssids': set()
    }


def ap_profile_count(path,ap):
    if ap['ap_profile'] not in ap_profile_dict:
        ap_profile_dict[ap['ap_profile']] = str(ap['ap_profile'])
        path['profile_count'] += 1
        #print(path['profile_count'])


def ap_profile_count_for_wlc(path,ap):
    if ap['ap_profile'] not in wlcprofiles:
        wlcprofiles[ap['ap_profile']] = str(ap['ap_profile'])
        path['profile_count'] += 1


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


def status_write(path,ap):
    if ap['state'] == 'authorized':
        path['authorized'] += 1
    if ap['state'] == 'discovered':
        if path == 'wlc':
            path['discovered'] += 1
    if ap['status'] == 'connected':
        path['connected'] += 1
    if ap['status'] == 'disconnected':
        path['disconnected'] += 1


def reboot_last_day_write(path,ap):
    if ap.get('reboot_last_day', False) == True:
        path['reboot_last_day'] += 1


def per_model_write(path,ap,campus):
    model = ap_profile_string(ap)[0]
    totalmodel = maindict['total']['ap_count']['per_model']

    if model == 'FAP221E-default' or model == 'FAP223E-default':
        model = model[:-8]

    if campus == False:

        if model not in totalmodel:
            totalmodel[model] = 1

        elif model in totalmodel:
            totalmodel[model] += 1

    if model not in path:
        path[model] = 1

    elif model in path:
        path[model] += 1


def ap_profile_string(ap):
    ap_profile = ap['ap_profile']
    cutstring = ''
    cutstring = ap_profile.split('_')
    campus = ''.join(cutstring[:-1])
    model = cutstring[-1]
    '''if campus == '':
        return model
    else:
        return [model, campus]'''
    return [model, campus]


def ap_write(ap):
    if ap['state'] != 'discovered':
        name = ap['name']
        maindict['ap'][name] = {
            'client_count': 0,
            'per_radio': {
                '1': 0,
                '2': 0
            },
            'ssids': set(),
            'ssid_count': 0
        }
        ssid_count(maindict['ap'][name],ap)
        appath = maindict['ap'][name]
        client_count(appath,ap,True)


def ap_read_trough(z):
    for ap in data:
        wlc_write(ap,z)
        ap_write(ap)


def total_write(z):
    zstring = str(z)
    wlc = maindict['wlc']['wlc'+zstring]
    total = maindict['total']
    total['ap_count']['total'] += wlc['ap_count']['total']
    total['ap_count']['status']['connected'] += wlc['ap_count']['status']['connected']
    total['ap_count']['status']['disconnected'] += wlc['ap_count']['status']['disconnected']
    total['ap_count']['status']['authorized'] += wlc['ap_count']['status']['authorized']
    total['ap_count']['status']['discovered'] += wlc['ap_count']['status']['discovered']
    total['ap_count']['reboot_last_day'] += wlc['ap_count']['reboot_last_day']

    total['campus_count'] += wlc['campus_count']
    total['profile_count'] += wlc['profile_count']
    total['client_count'] += wlc['client_count']
    total['ssid_count'] += wlc['ssid_count']


def wlc_write(ap,z):
    zstring = str(z)
    wlc = maindict['wlc']['wlc'+zstring]
    wlc['ap_count']['total'] += 1
    status_write(wlc['ap_count']['status'],ap)
    reboot_last_day_write(wlc['ap_count'],ap)
    per_model_write(wlc['ap_count']['per_model'],ap,False)
    ap_profile_count_for_wlc(maindict['wlc']['wlc'+zstring],ap)
    '''if ap['ap_profile'] not in ap_profile_dict:
        ap_profile_dict[ap['ap_profile']] = str(ap['ap_profile'])
        wlc['profile_count'] += 1'''
    client_count(wlc,ap,False)
    ssid_count(wlc,ap)


def filter_dict(data,key):
    if key in data:
        data.pop(key)
    for x in data:
        if isinstance(data[x],dict):
            filter_dict(data[x],key)

def main(ssidapi,productionapiarray):
    global data, datassid
    init()
    z = 0
    for wlc in productionapiarray:
        ssidurl = ssidapi[z]
        ssidresponse = requests.get(ssidurl)
        datassid = (ssidresponse.json()['results'])

        url = productionapiarray[z]
        response = requests.get(url)
        data = (response.json()['results'])
        z += 1
        wlc_create(z)
        ap_campus_counter(z)
        ap_read_trough(z)
        total_write(z)

    maindict['total']['wlc_count'] = z
    filter_dict(maindict,'ssids')
    return maindict


if __name__ == "__main__":
    print(json.dumps(main(ssidapi,productionapiarray), indent = 4, sort_keys = True))
