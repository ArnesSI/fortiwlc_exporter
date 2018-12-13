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
    return model, campus, ap_profile


def parse_ap_data(ap_data, wlc_name):
    """ Parses AP data from WLC API into format suitable for metric export """
    name = ap_data['name']
    model, campus, profile = ap_profile_string(ap_data)
    ap = [
        wlc_name,
        ap_data['name'],
        ap_data['status'],
        ap_data['state'],
        profile,
        model,
    ]
    if campus:
        ap.append(campus)
    return ap


def parse_wifi_name(wifi_name):
    """ Returns wifi name and ssid """
    return (wifi_name, wifi_name.split('_', maxsplit=1)[-1])
