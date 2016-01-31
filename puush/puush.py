# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import hashlib
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
    # ASCII here is fine as long as the Puush server only supports ASCII.
    response = raw_api_request(endpoint, **kwargs).decode('ASCII')
    return [line.split(',') for line in response.strip().split('\n')]

def md5_file(f):
    md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(8192), b''):
        md5.update(chunk)
    f.seek(0)
    return md5.hexdigest()

def auth(api_key_or_email, password=None):
    # E-mail and password authentication
    if password is not None:
        email = api_key_or_email
        data = {
            'e': email,
            'p': password
        }
    # Direct API key authentication
    else:
        api_key = api_key_or_email
        data = {
            'k': api_key
        }
    
    res = api_request('auth', data=data)[0]
    
    if res[0] == '-1':
        if password is not None:
            raise AuthenticationError(
                "No Puush account with the provided credentials.")
        else:
            raise AuthenticationError("Invalid API key.")
    
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
        """A Puush Account can be instantiated either with API key or
        e-mail and password.
        
        Parameters:
            * api_key_or_email: API key if it's the only argument, e-mail if
              password parameter is present.
            * password (optional): The password for the Puush account if
              api_key_or_email is an e-mail address.
        """
        # E-mail and password authentication
        if password is not None:
            email = api_key_or_email
            self.is_premium, self._api_key, _, _ = auth(email, password)
        # Direct API key authentication
        else:
            self._api_key = api_key_or_email
            auth(self._api_key)
    
    @property
    def is_premium(self):
        """Whether the Puush account has premium status or not.
        
        True if the account is premium, False if not.
        Only available if instantiated with e-mail and password.
        """
        try:
            return self._is_premium
        except AttributeError:
            raise PuushError(
                "Account.is_premium is unavailable, since the "
                "Account was initialized with an API key "
                "and not login credentials."
            )
    
    @is_premium.setter
    def is_premium(self, value):
        self._is_premium = value
    
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
        """Upload a file to the Puush account.
        
        Parameters:
            * f: The file. Either a path to a file or a file-like object.
        """
        if hasattr(f, 'read'):
            needs_closing = False
        else:
            f = open(f, 'rb')
            needs_closing = True
        # The Puush server can't handle non-ASCII filenames.
        # The official Puush desktop app actually substitutes ? for
        # non-ISO-8859-1 characters, which helps some Unicode filenames,
        # but some are still let through and encounter server errors.
        # Try uploading a file named åäö.txt through the desktop app -
        # it won't work. It's better to let this Python API do that,
        # however, with the behavior probably intended in the desktop app.
        filename = os.path.basename(f.name).encode('ascii', 'replace')
        filename = filename.decode('ascii') # Requests doesn't like bytes
        md5 = md5_file(f)
        
        data = {
            'z': 'meaningless',
            'c': md5
        }
        files = {
            'f': (filename, f)
        }
        
        res = self._api_request('up', data=data, files=files)[0]
        if res[0] == '-1':
            raise PuushError("File upload failed.")
        elif res[0] == '-3':
            raise PuushError("File upload failed: hash didn't match with "
                "the file the server received.")
        
        if needs_closing:
            f.close()
        
        _, url, id, size = res
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self._File(id, url, filename, now, 0)
    
    def delete(self, id):
        """Delete a file.
        
        Parameters:
            * id: The Puush ID of the file to delete.
        """
        res = self._api_request('del', data={'i': id})[0]
        if res[0] == '-1':
            raise PuushError("File deletion failed.")
    
    def thumbnail(self, id):
        """Get the 100x100 thumbnail of a file. Return the raw PNG data.
        
        Parameters:
            * id: The Puush ID of the file to get the thumbnail of.
        """
        res = self._raw_api_request('thumb', data={'i': id})
        if not res:
            raise PuushError("Getting thumbnail failed.")
        return res

    def history(self):
        """Get the latest 10 files uploaded to the account.
        Return a list of Puush File objects.
        """
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
        * url:         The URL to access the file.
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
            self.filename.encode(sys.stdout.encoding, 'replace').decode(
                sys.stdout.encoding)
        )
    
    def delete(self):
        """Delete the file from Puush."""
        self._account.delete(self.id)
    
    def thumbnail(self):
        """Get the 100x100 thumbnail of the file. Return the raw PNG data."""
        return self._account.thumbnail(self.id)
