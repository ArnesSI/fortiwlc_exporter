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


def parse_ap_data(ap_data, wlc_name):
    name = ap_data['name']
    ap = {
        'name': name,
        'campus_name': ap_profile_string(ap_data)[1],
        'profile_name': ap_profile_string(ap_data)[2],
        'model': ap_profile_string(ap_data)[0],
        'wlc': wlc_name,
        'status': ap_data.get('status', None),
        'state': ap_data['state'],
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
    client_count(ap, ap_data, True)
    return ap
