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


def get_ap_os_version(ap):
    """Parses os_version from AP data

    Removes model from start of os version if found.
    
    Args:
        ap (dict): ap data returned from FortiOS managed-ap REST endpoint
    
    Returns:
        str: OS version on 'unknown' id not detected
    """

    if 'os_version' not in ap:
        return 'unknown'
    return ap['os_version'].split('-', 1)[-1]


def get_ap_serial_number(ap):
    """Parses serial number from AP data

    Args:
        ap (dict): ap data returned from FortiOS managed-ap REST endpoint
    
    Returns:
        str: serial number or 'unknown' id not found
    """

    return ap.get('serial', 'unknown')


def parse_ap_data(ap_data, wlc_name):
    """ Parses AP data from WLC API into format suitable for metric export """
    model, campus, profile = ap_profile_string(ap_data)
    os_version = get_ap_os_version(ap_data)
    serial_number = get_ap_serial_number(ap_data)
    ap = [
        wlc_name,
        ap_data['name'],
        ap_data['status'],
        ap_data['state'],
        os_version,
        serial_number,
        profile,
        model,
    ]
    if campus:
        ap.append(campus)
    return ap


def parse_wifi_name(wifi_name):
    """ Returns wifi name and ssid """
    return (wifi_name, wifi_name.split('_', maxsplit=1)[-1])
