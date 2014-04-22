Tutorial
========

The assets directories
----------------------

Django Gears searches for assets in the defined assets directories.
By default, this includes all ``assets`` folders defined in your installed
applications. You'll find this approach familiar if you've used Django's
application template loader or static files finder.

For this tutorial, imagine you have an assets directory like this::
    
    assets/
        css/
            buttons.css
            styles.css
        js/
            script.js
            app.js
        vendor/
            jquery.js
            underscore.js


Using directives
----------------

The primary Gears preprocessor is based on directives. Directives are
a way to handle dependencies in your css and scripts.

For example, ``script.js`` in the example folder may look like this::

    /* Dependencies:
     *= require ../vendor/jquery
     *= require ../vendor/underscore
     *= require app
    */

Each line that starts with ``*=`` is a directive. Directives let you
include files, trees, or directory contents into a single file. Directives
are always relative to the file that contains them.

For another example, the style.css file may look like this::

    /* Dependencies:
     *= require buttons.css
     *= require_self
    */

    # more styles here

You can see a list of `available directives here <https://github.com/gears/gears# features>`_.


Adding scripts and css to templates
-----------------------------------

Now that the script.js and styles.css files are defined they can be
included in your templates. You can do this with the ``{% gears %}``
template tags.

.. code-block:: django

    {% load gears %}
    {% css_asset_tag "css/style.css" %}
    {% js_asset_tag "js/script.js" %}


What happened?
~~~~~~~~~~~~~~

Gears will construct link or script tags to the proper assets. When using
the :func:`~django_gears.urls.gears_urlpatterns`, the :func:`django_gears.views.serve` view will be
called. This will process and serve the assets at the time of the request.
You can edit the assets and reload the page to immediately see the changes.

For production, the assets will be pre-built using the ``collectassets``
command. The urls will point to these files that should be served as
static files by the web server. We'll discuss this more later.
