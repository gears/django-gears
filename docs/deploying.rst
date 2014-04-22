Deploying
=========

The :func:`~django_gears.urls.gears_urlpatterns` work great in development,
but you don't want to build files during the request cycle in production.
Instead, the files should be built once and served as static files by your
web server. The ``collectassets`` command lets you do that.


Collecting assets
-----------------

The ``collectassets`` command is a `Django management command`_ that is
invoked using the manage.py script::

    python manage.py collectassets


.. _Django management command: https://docs.djangoproject.com/en/dev/ref/django-admin/

This command collects all public assets, processes them, and saves them to
the directory specified by the :setting:`GEARS_ROOT` setting.

In addition to processing the assets, Gears adds a ``.manifest.json`` file
to the directory root. An example manifest file looks like::

    {
      "files": {
        "css/styles.css": "css/style.588bb73e7fff720ac360b924fd9b33ddd2fa71c7.css", 
        "js/script.js": "js/script.d78f84d27230e157031fc8ed26d1099f44d878dd.js"
      }
    }

This file is a map between asset names and processed files. When an
asset is included using a ``{% gears %}`` tag in production, instead of
producing a url to the development view, it produces a url to the asset as
specified in the manifest file.


Defining public assets
----------------------

When ``collectassets`` is run, Gears will only process assets that are
public. Gears considers any asset public that matches the
:setting:`GEARS_PUBLIC_ASSETS` setting.

For instance, you may have a script.js file that includes many dependencies.
After processing script.js, there is no need to Gears to additionally
process the individual dependencies and collect them as separate files
into :setting:`GEARS_ROOT`. This is an optimization that results in faster
build times.

The default rules for collecting public assets:

* include all files that either aren't css or javascript or aren't set to
  compile to css or javascript (less, style, coffee, etc.)
* include css/style.css
* include js/script.js

If you namespace your assets, or use a different naming convention, you'll
want to specify your own public asset patterns. For instance, if you want
to process all files mapping to site.css or site.js, you could do::

    GEARS_PUBLIC_ASSETS = (
        lambda path: not any(path.endswith(ext) for ext in ('.css', '.js')),
        r'site\.css$',
        r'site\.js$',
    )


Serving files with your web server
----------------------------------

By default, Django Gears collects assets into the ``STATIC_ROOT``
directory. If your web server is configured to serve static files already,
no additional configuration is needed. If you haven't configured this,
you can follow Django's advice on `deploying static files`_ or use a
wsgi app like `dj‑static`_.

.. _deploying static files: https://docs.djangoproject.com/en/dev/howto/static-files/deployment/
.. _dj‑static: https://github.com/kennethreitz/dj-static

If you specify a custom directory in :setting:`GEARS_ROOT`, you'll need to
update your server accordingly.
