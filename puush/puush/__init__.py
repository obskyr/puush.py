# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

"""puush.py

A Python module to access the Puush (http://puush.me/) API.
"""

import sys
import requests

if sys.version_info[0] >= 3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

PUUSH_API_URL = "https://puush.me/api/"

def api_request(endpoint, **kwargs):
    r = requests.post(urljoin(PUUSH_API_URL, endpoint), **kwargs)
    return [line.split(',') for line in r.text.split('\n')]

def auth(email, password):
    res = api_request('auth', data={
        'e': email,
        'p': password
    })[0]
    
    if res[0] == '-1':
        raise AuthenticationError(
            "No Puush account with the provided credentials.")
    
    is_premium = bool(int(res[0]))
    api_key = res[1]
    # Note: Nothing is done with the `expires` data right now - to do
    # is to get hold of a premium account and figure out its format.
    expires = res[2]
    size_sum = res[3] # What might this be...?
    
    return is_premium, api_key, expires, size_sum

class PuushError(Exception):
    pass

class AuthenticationError(PuushError, ValueError):
    pass

class Account(object):
    def __init__(self, api_key_or_email, password=None):
        # E-mail and password authentication
        if password is not None:
            email = api_key_or_email
            self.is_premium, self._api_key, _, _ = auth(email, password)
        # Direct API key authentication
        else:
            self._api_key = api_key_or_email
    
    is_premium = None
    
    def _api_request(self, endpoint, **kwargs):
        data = kwargs.pop('data', {})
        data.update({'k': self._api_key})
        api_request(endpoint, data=data, **kwargs)
    
    def upload(self, f):
        if hasattr(f, 'read'):
            needs_closing = False
        else:
            f = open(f, 'rb')
            needs_closing = True
        
        data = {
            'z': 'meaningless'
        }
        files = {
            'f': f
        }
        
        self._api_request('up', data=data, files=files)
        
        if needs_closing:
            f.close()