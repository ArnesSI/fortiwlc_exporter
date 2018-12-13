import configparser


DEFAULTS = {
    'port': 9118,
    'debug': False,
    'workers': 2,
    'username': '',
    'password': '',
}

CONFIG = {}


def get_config(file, extra=None):
    config_parser = configparser.ConfigParser()
    config_parser.read_file(file)
    if not config_parser.has_section('main'):
        config_parser.add_section('main')

    for opt, default_value in DEFAULTS.items():
        if isinstance(default_value, bool):
            CONFIG[opt] = config_parser['main'].getboolean(opt, default_value)
        elif isinstance(default_value, int):
            CONFIG[opt] = config_parser['main'].getint(opt, default_value)
        else:
            CONFIG[opt] = config_parser['main'].get(opt, default_value)
        CONFIG[opt] = getattr(extra, opt, CONFIG[opt])

    wlcs = []
    for section in config_parser.sections():
        if section == 'main':
            continue
        wlc_params = dict(config_parser[section])
        wlc_params['name'] = section
        if 'username' not in wlc_params:
            wlc_params['username'] = CONFIG['username']
        if 'password' not in wlc_params:
            wlc_params['password'] = CONFIG['password']
        wlcs.append(wlc_params)
    CONFIG['wlcs'] = wlcs

    return CONFIG
