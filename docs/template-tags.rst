Asset template tags
===================

Loading assets
--------------

Django Gears provides two template tags for use in templates: one for
css and one for javascript.

The usage of these tags looks like:

.. code-block:: django

    {% load gears %}
    {% css_asset_tag "css/style.css" %}
    {% js_asset_tag "js/script.js" %}

This outputs script and link tags like the following:

.. code-block:: html

    <link rel="stylesheet" href="/<staticroot>/css/style.5d9fedbb2fdb499586390e3969277fe4208122b8.css">
    <script src="/<staticroot>/js/script.2b4ef7ddce5b87d9b7fe6c7b5df40d32b923359f.js"></script>


Debug settings
--------------

If :setting:`GEARS_DEBUG` is true, the directives will not be processed
into a single file. Instead, each asset will be processed and linked to
individually.

For example, consider the directives:

::

    /*
     *= require jquery
     *= require underscore
    */

The output when :setting:`GEARS_DEBUG` is true looks like:

.. code-block:: html

  <script src="/<staticroot>/jquery.js?body=1&v=1396028840.58"></script>
  <script src="/<staticroot>/underscore.js?body=1&v=1396035841.85"></script>
  <script src="/<staticroot>/script.js?body=1&v=1396035841.85"></script>

This behavior can also be triggered from within a template by adding a
``debug`` argument to the asset tags:

.. code-block:: django

    {% css_asset_tag "css/style.css" debug %}
    {% js_asset_tag "js/script.js" debug %}
