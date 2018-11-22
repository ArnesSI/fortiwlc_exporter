import requests
import json
import sys
from pprint import pprint

from .fortiwlc import FortiWLC


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


def main(wlc_group):
    global data, datassid
    init()

    for wlc_name, api_key in wlc_group:
        data = FortiWLC(wlc_name, api_key).get_managed_ap()
        ap_read_trough(wlc_name)
    return maindict


#if __name__ == "__main__":
#    wlcarray = sys.argv[1]
#    print(json.dumps(main(ssidapi,wlcarray), indent = 4, sort_keys = False))
