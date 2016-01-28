"""puush.py, a Python wrapper for the Puush API. 

Usage:
    import puush
    account = puush.Account("my_api_key")
    # Or...
    account = puush.Account("name@example.com", "bestpassword")
    account.upload("super_cool_picture.png")
"""

from .puush import Account
