import os
import requests
import warnings
import contextlib
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning

load_dotenv('.env')

__old_merge_environment_settings = requests.Session.merge_environment_settings
__auth = HTTPBasicAuth(os.environ.get('ILO_USER'), os.environ.get('ILO_PASSWORD'))

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):

        opened_adapters.add(self.get_adapter(url))

        settings = __old_merge_environment_settings(
            self, url, proxies, stream, verify, cert
        )
        settings["verify"] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = __old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass

def __get_2darray(url, category, name, value):
    arr = [[], []]
    with no_ssl_verification():
        req = requests.get(url, auth=__auth)
    data = json.loads(req.text)
    for temp in data[category]:
        arr[0].append(temp[name])
        arr[1].append(temp[value])
    return arr

def __get_single(url, category):
    with no_ssl_verification():
        req = requests.get(url, auth=__auth)
    data = json.loads(req.text)
    arr = data[category]
    return arr

def get_temperature(url):
    temp_url = url + 'rest/v1/Chassis/1/Thermal'
    return __get_2darray(temp_url, 'Temperatures', 'Name', 'CurrentReading')

def get_fans(url):
    fans_url = url + 'rest/v1/Chassis/1/Thermal'
    return __get_2darray(fans_url, 'Fans', 'FanName', 'CurrentReading')

def get_watts(url):
    watts_url = url + 'rest/v1/Chassis/1/Power'
    return __get_single(watts_url, 'PowerConsumedWatts')

def get_hostname(url):
    host_url = url + 'rest/v1/Managers/1/NetworkService'
    return __get_single(host_url, 'HostName')