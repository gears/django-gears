Asset finders
=============

Django Gears searches for assets to build in the defined assets directories.
By default, this includes:

* all assets directories in your installed applications
* all assets directories listed in the  :setting:`GEARS_DIRS` setting

We'll cover how both of these work below.


Application finder
------------------

Consider a directory structure like the following, where ``myapp1``
and ``myapp1`` are installed applications::

    myapp1/
      assets/
        js/
          script.js
          app.js

    myapp2/
      assets/
        js/
          test.js

Next, consider that script.js has the following directives::

    /*
     *= require test
     *= require app
    */

When script.js is processed it will include test.js from ``myapp2`` and
app.js from ``myapp1``.


How does this happen?
~~~~~~~~~~~~~~~~~~~~~

Directives, as written, are always relative to the asset file. The idea of
relative isn't solely based on the filesystem, though. In the above example,
both ``myapp1/assets`` and ``myapp2/assets`` are on the search paths. This
means when test.js isn't found in the current directory, the directive
processor continues on through the rest of the directories on the search
path. Here, it is found in myapp2.

Note, Gears will use the first asset it finds that matches the given path.
Therefore, if you have multiple assets whose name and location is the same,
Gears won't distinguish between them. The easiest way to ensure this doesn't happen is to place assets in custom
named directories within the assets folder.


File System Finder
------------------

In addition to the application finder, Django Gears will look for static
files in specified directories in the filesystem. These directories are
controlled through the :setting:`GEARS_DIRS` setting.

For example, you may add an assets directory in your project root:

.. code-block:: python

    import os
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    GEARS_DIRS = (
        os.path.join(SITE_ROOT, "assets"),
    )

By default, the file system finder has precedence over the application
finders.


Configuring finders
-------------------

If you want to configure or add custom finders of your own, see the
docs on the :setting:`GEARS_FINDERS` setting.
