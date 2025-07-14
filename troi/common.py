import os

import yaml
from troi.troi_api.api import Client

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "troi_billing", "config.yaml")


def load_config():
    with open(CONFIG_FILE, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg['credentials'], cfg['config'] if 'config' in cfg else {}


def get_client(credentials):
    return Client(credentials['url'], credentials['username'], credentials['api_token'])
