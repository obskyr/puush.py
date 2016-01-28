puush.py
========

``puush.py`` is a Python library for interfacing with `Puush <https://puush.me>`__, a file host, web app, and desktop app with a great quick-upload screenshot feature. It's very simple to use:

.. code:: python

    import puush
    account = puush.Account("my_api_key")
    account.upload("super_cool_picture.png")

To use ``puush.py``, you will need either login credentials (e-mail and password), or an API key, which can be obtained from `your account settings page <https://puush.me/account/settings>`__.

Installation
------------

Simply install it with `pip <https://pip.pypa.io/en/latest/installing/>`__, as following:

::

    pip install puush.py

Documentation
-------------

Mainly, you will be using the ``puush.Account`` class. It uses ``puush.File`` objects, however, so both of these are detailed below. On failure, all methods raise a ``puush.PuushError``.

``puush.Account(api_key_or_email[, password=None])``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialize an ``Account`` using either an API key or login credentials:

.. code:: python

    # With API key
    account = puush.Account("my_api_key")
    # With login credentials
    account = puush.Account("name@example.com", "bestpassword")

If the API key or credentials are invalid, a ``puush.AuthenticationError`` (which subclasses ``puush.PuushError``) will be raised.

``puush.Account.upload(self, f)``
'''''''''''''''''''''''''''''''''
Upload a file to the Puush account. The only parameter, ``f``, can be either a path to a file or a file-like object. Return a ``puush.File``.

``puush.Account.delete(self, id)``
''''''''''''''''''''''''''''''''''
Delete the file with the ID ``id`` from the Puush account.

Also consider using ``puush.File.delete`` if you already have a ``File``.

``puush.Account.thumbnail(self, id)``
'''''''''''''''''''''''''''''''''''''
Get the 100x100px thumbnail of the file with the ID ``id``, and return its raw PNG data.

Also consider using ``puush.File.thumbnail`` if you already have a ``File``.

``puush.Account.history(self)``
'''''''''''''''''''''''''''''''
Return a list of the Puush account's last 10 (or fewer, if the account has fewer) uploads. Each entry is a ``puush.File``.

-----------------------------------------------------

``puush.File(id, url, filename, upload_time, views)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A file uploaded to Puush. Not meant to be initialized outside of the library.

``puush.File.delete(self)``
'''''''''''''''''''''''''''
Delete the file from Puush.

``puush.File.thumbnail(self)``
''''''''''''''''''''''''''''''
Get the 100x100 thumbnail of the file. Return the raw PNG data.

``puush.File.id``
'''''''''''''''''
The Puush ID of the uploaded file. Is unique to the file, and can be used with ``puush.Account`` methods.

``puush.File.url``
''''''''''''''''''
The URL to access the file.

``puush.File.filename``
'''''''''''''''''''''''
The file's original filename.

``puush.File.upload_time``
''''''''''''''''''''''''''
The file's upload time, formatted "YYYY-MM-DD HH:MM:SS".

``puush.File.views``
''''''''''''''''''''
How many times the file has been accessed.

Special thanks
--------------

I would like to thank `blha303 <https://github.com/blha303>`__ for the `Puush API documentation <https://github.com/blha303/puush-linux/blob/3c443e7aa70f823625d40d1f8c27386297d29b45/apiDocumentation.md>`__. Having it definitely saved me a lot of time reverse-engineering the desktop app.

Contact
-------

If there's a bug with the library or a feature you'd like, please `open an issue <https://github.com/obskyr/puush.py/issues>`__ on GitHub. 

If you want to ask questions about the library, or just want to talk to me about... anything, really, you can do so through any of these:

* Tweet `@obskyr <https://twitter.com/obskyr>`__ on Twitter
* `E-mail me <mailto:powpowd@gmail.com>`__

To get a quick answer, Twitter is your best bet.

Enjoy!
