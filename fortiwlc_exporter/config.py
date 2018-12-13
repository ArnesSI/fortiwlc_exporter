import configparser


DEFAULTS = {
    'port': 9118,
    'debug': False,
}


def get_config(file):
    config_parser = configparser.ConfigParser()
    config_parser.read_file(file)
    wlcs = []
    for section in config_parser.sections():
        if section == 'main':
            continue
        wlc_params = dict(config_parser[section])
        wlc_params['name'] = section
        wlcs.append(wlc_params)
    config = {'wlcs': wlcs}
    if config_parser.has_section('main'):
        for opt, default_value in DEFAULTS.items():
            if isinstance(default_value, bool):
                config[opt] = config_parser['main'].getboolean(opt, default_value)
            elif isinstance(default_value, int):
                config[opt] = config_parser['main'].getint(opt, default_value)
            else:
                config[opt] = config_parser['main'].get(opt, default_value)
    else:
        config.update(DEFAULTS)
    return config
