Installation
============

Get the code
------------

You can install Django Gears with pip_::

    $ pip install django-gears

It's strongly recommended to install Django Gears within an activated
virtualenv_.

If you want to work with the latest version of Django Gears, install it from
the public repository::

    $ pip install -e git+https://github.com/gears/django-gears@develop#egg=django-gears

.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://virtualenv.org/


Add to settings
---------------

Add ``django_gears`` to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = (
        #  ...
        'django_gears',
        #  ...
    )


Configure development urls
--------------------------

.. code-block:: python

    from django_gears.urls import gears_urlpatterns

    # url definitions here

    urlpatterns += gears_urlpatterns()

.. note::

    If you use Django's `staticfiles_urlpatterns`_, you should replace that
    with gears_urlpatterns. Django Gears falls back to serving static files
    when matching assets aren't found.

.. _staticfiles_urlpatterns: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/# django.contrib.staticfiles.urls.staticfiles_urlpatterns

Moving on
---------

Congratulations. You have a working installation. Now, continue to the
tutorial to learn how to use Gears in your templates.
