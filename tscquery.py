# The tscquery library for Python 3
# Author: Jack Rosenthal, Steamboat Networks
# Don't try to run this file itself, it is just a library
# Instead, import it in your script.
#
# License: If you modify this script, be sure to share the
# source with others and retain attribution to the original
# author. So as long as you do that, free use is granted.
#
# Depends on requests, requests_cache, and yaml. You can
# install all of these through pip.

import requests
import yaml

# You will need to make the file 'config.yaml' with your own api keys. See
# the file 'config_example.yaml' for an example.
with open("config.yaml", "r") as f:
    config = yaml.load(f)

# This will cache our HTTP requests. This saves money!
if config["caching"]["enabled"] == True:
    import requests_cache
    requests_cache.install_cache("query_cache", backend="sqlite", expire_after=config["caching"]["expire_after"])

# Shortcut functions for generating URLs for the api's
def lrn_api_url(tn, ani=config['alcazar']['default_ani'], extended=config['alcazar']['default_extended'], output='json', server=config['alcazar']['default_server'], apikey=config['alcazar']['apikey']):
    return "http://api{}.east.alcazarnetworks.com/api/lrn?tn={}&ani={}&extended={}&output={}&key={}"\
            .format(server, tn, ani, 'true' if extended else 'false', output, apikey)

def cnam_api_url(tn, output='json'):
    return "https://api.opencnam.com/v2/phone/{}?format={}&account_sid={}&auth_token={}"\
            .format(tn, output, config['opencnam']['sid'], config['opencnam']['token'])

# The lrn_query class handles the api requests and parsing the data for you
class lrn_query:
    def __init__(self, tn, ani=config['alcazar']['default_ani'], server=config['alcazar']['default_server'], extended=config['alcazar']['default_extended']):
        self.tn = tn
        self.ani = ani
        self.server = server
        self.extended = extended
        self.request = requests.get(lrn_api_url(tn=self.tn, ani=self.ani, server=self.server, extended=self.extended))

    @property
    def data(self):
        return self.request.json()

    @property
    def lrn(self):
        return self.data["LRN"]

    @property
    def exchange(self):
        return self.data["LRN"][:-4]

    @property
    def ocn(self):
        if self.extended:
            return self.data["OCN"]
        return None

    @property
    def lata(self):
        if self.extended:
            return int(self.data["LATA"])
        return None

    @property
    def city(self):
        if self.extended:
            return self.data["CITY"]
        return None

    @property
    def state(self):
        if self.extended:
            return self.data["STATE"]
        return None

    @property
    def lec(self):
        if self.extended:
            return self.data["LEC"]
        return None

    @property
    def linetype(self):
        if self.extended:
            return self.data["LINETYPE"]
        return None

    @property
    def intrastate(self):
        if self.extended:
            return bool(self.data["JURISDICTION"] == "INTRASTATE" or self.data["JURISDICTION"] == "INDETERMINATE")
        return False

# The cnam_query class is very simmilar
class cnam_query:
    def __init__(self, tn):
        self.tn = tn
        self.request = requests.get(cnam_api_url(tn=self.tn))

    @property
    def data(self):
        return self.request.json()

    @property
    def name(self):
        return self.data['name']

    @property
    def price(self):
        return float(self.data['price'])
