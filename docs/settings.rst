Settings
========

.. setting:: GEARS_CACHE

GEARS_CACHE
-----------

This defines the cache used in the Gears environment. The default
values is ``gears.cache.SimpleCache``.


.. setting:: GEARS_COMPRESSORS

GEARS_COMPRESSORS
-----------------

A mapping of mimetype to compressors. For example:

.. code-block:: python

    GEARS_COMPRESSORS = {
        'application/javascript': 'gears_uglifyjs.UglifyJSCompressor',
        'text/css': 'gears_clean_css.CleanCSSCompressor',
    }

By default, this setting is equal to ``{}``. No compressors are defined.


.. setting:: GEARS_COMPILERS

GEARS_COMPILERS
---------------

A mapping of file extension to compilers. For example:

.. code-block:: python

    GEARS_COMPILERS = {
        '.styl': 'gears_stylus.StylusCompiler',
        '.coffee': 'gears_coffeescript.CoffeeScriptCompiler',
    }

By default, this setting is equal to ``{}``. No compilers are defined.


.. setting:: GEARS_DEBUG

GEARS_DEBUG
-----------

Whether Gears is in debug mode or not. Defaults to the value of
``settings.DEBUG``. This affects how the template tags process assets.
See the :doc:`template-tags` docs for more information.


.. setting:: GEARS_DIRS

GEARS_DIRS
----------

The list of directories to search for assets. This is used when the
``gears.finders.FileSystemFinder`` is specified in
:setting:`GEARS_FINDERS`. Defaults to ``[]``. No directories are defined.


.. setting:: GEARS_FINDERS

GEARS_FINDERS
-------------

The list of finders to use when searching for assets. The default finders
are:

.. code-block:: python

    GEARS_FINDERS = (
        ('gears.finders.FileSystemFinder', {
            'directories': getattr(settings, 'GEARS_DIRS', ()),
        }),
        ('django_gears.finders.AppFinder', {}),
    )


.. setting:: GEARS_FINGERPRINTING

GEARS_FINGERPRINTING
--------------------

Whether Gears should save a fingerprinted version of the asset in the
build directory. A fingerprint is based on the contents of the file and
thus unique for each version of it. Fingerprinted files are also added to
the ``.manifest.json`` file. Defaults to ``True``.


.. setting:: GEARS_GZIP

GEARS_GZIP
----------

Whether Gears should gzip processed files at the end of the build process.
Defaults to ``False``.


.. setting:: GEARS_MIMETYPES

GEARS_MIMETYPES
---------------

The mimetypes for asset file extensions. Mimetypes are used by post and
preprocessors as well as compressors. The default mimetypes are:

.. code-block:: python

    GEARS_MIMETYPES = {
        '.css': 'text/css',
        '.js': 'application/javascript',
    }


.. setting:: GEARS_POSTPROCESSORS

GEARS_POSTPROCESSORS
--------------------

The list of postprocessors to run when assets are served or collected.
The default postprocessors are:

.. code-block:: python

    GEARS_POSTPROCESSORS = {
        'text/css': 'gears.processors.HexdigestPathsProcessor',
    }


.. setting:: GEARS_PREPROCESSORS

GEARS_PREPROCESSORS
-------------------

The list of preprocessors to run when assets are served or collected. The
default preprocessors handle dependency management through directives.

.. code-block:: python

    GEARS_PREPROCESSORS = {
        'text/css': 'gears.processors.DirectivesProcessor',
        'application/javascript': 'gears.processors.DirectivesProcessor',
    }


.. setting:: GEARS_PUBLIC_ASSETS

GEARS_PUBLIC_ASSETS
-------------------

The patterns that define public assets. Only assets matching one of these
patterns will be processed when ``collectassets`` is run. The default
values are:

.. code-block:: python

    GEARS_PUBLIC_ASSETS = (
        lambda path: not any(path.endswith(ext) for ext in ('.css', '.js')),
        r'^css/style\.css$',
        r'^js/script\.js$',
    )

Each pattern can either be a regular expression or a function that takes a
path and returns a boolean.


.. setting:: GEARS_ROOT

GEARS_ROOT
----------

The directory where built assets are stored. Defaults to
``settings.STATIC_ROOT``.


.. setting:: GEARS_URL

GEARS_URL
---------

The url to serve processed assets under. Defaults to ``settings.STATIC_URL``.
