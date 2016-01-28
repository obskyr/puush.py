"""puush.py

A Python module for the Puush (http://puush.me/) API.

Usage:
    import puush
    account = puush.Account("my_api_key")
    # Or...
    account = puush.Account("name@example.com", "bestpassword")
    account.upload("super_cool_picture.png")
"""

# File really only in here for help() and dir()'s sake.

from .puush import Account, File, PuushError, AuthenticationError
