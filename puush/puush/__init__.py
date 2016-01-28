# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

"""puush.py

A Python module to access the Puush (http://puush.me/) API.
"""

import os
import sys
import requests
from datetime import datetime

if sys.version_info[0] >= 3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

PUUSH_API_URL = "https://puush.me/api/"

def raw_api_request(endpoint, **kwargs):
    r = requests.post(urljoin(PUUSH_API_URL, endpoint), **kwargs)
    return r.content

def api_request(endpoint, **kwargs):
    response = raw_api_request(endpoint, **kwargs)
    return [line.split(',') for line in response.strip().split('\n')]

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
    """A Puush account."""
    def __init__(self, api_key_or_email, password=None):
        # E-mail and password authentication
        if password is not None:
            email = api_key_or_email
            self.is_premium, self._api_key, _, _ = auth(email, password)
        # Direct API key authentication
        else:
            self._api_key = api_key_or_email
    
    is_premium = None
    
    def _raw_api_request(self, endpoint, **kwargs):
        data = kwargs.pop('data', {})
        data.update({'k': self._api_key})
        return raw_api_request(endpoint, data=data, **kwargs)
    
    def _api_request(self, endpoint, **kwargs):
        data = kwargs.pop('data', {})
        data.update({'k': self._api_key})
        return api_request(endpoint, data=data, **kwargs)
    
    def _File(self, *args, **kwargs):
        return File(account=self, *args, **kwargs)
    
    def upload(self, f):
        """Upload a file to the account.
        
        Parameters:
            * f: The file. Either a path to a file or a file-like object.
        """
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
        
        res = self._api_request('up', data=data, files=files)[0]
        if res[0] == '-1':
            raise PuushError("File upload failed.")
        
        if needs_closing:
            f.close()
        
        _, url, id, size = res
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self._File(id, url, os.path.basename(f.name), now, 0)
    
    def delete(self, id):
        res = self._api_request('del', data={'i': id})[0]
        if res[0] == '-1':
            raise PuushError("File deletion failed.")
    
    def thumbnail(self, id):
        res = self._raw_api_request('thumb', data={'i': id})
        if not res:
            raise PuushError("Getting thumbnail failed.")
        return res

    def history(self):
        res = self._api_request('hist')
        if res[0][0] == '-1':
            raise PuushError("History retrieval failed.")
        
        files = []
        for line in res[1:]:
            id, upload_time, url, filename, views, _ = line
            files.append(self._File(id, url, filename, upload_time, views))
        return files

class File(object):
    """A file uploaded to a Puush account.
    
    Properties:
        * id:          The unique Puush ID of the file.
        * url:         The url to access the file.
        * filename:    The file's original filename.
        * upload_time: The file's upload time, formatted "YYYY-MM-DD HH:MM:SS".
        * views:       How many times the file has been accessed.
    """
    def __init__(self, id, url, filename, upload_time, views, account):
        self._account = account
        
        self.id = id
        self.url = url
        self.filename = filename
        self.upload_time = upload_time
        self.views = int(views)
    
    def __repr__(self):
        return "<Puush File {}: \"{}\">".format(
            self.id,
            self.filename.encode(sys.stdout.encoding, 'replace')
        )
    
    def delete(self):
        self._account.delete(self.id)
    
    def thumbnail(self):
        return self._account.thumbnail(self.id)
