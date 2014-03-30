Asset views
===========

Serving assets in development
-----------------------------

.. module:: django_gears.views

.. py:function:: serve(request, path, **kwargs)

Django Gears provides the :py:func:`serve` view for use in development.
This view will process and serve any matching assets on the fly. This means
you can simply reload your pages to see the latest changes.

Further, if no matching asset is found, :func:`serve` falls back to Django's
``staticfiles.views.serve`` view. This means your application can happily
serve static files alongside Gear's assets.

The easiest way to make use of the :func:`serve` view in your application
is to use the included :func:`~django_gears.urls.gears_urlpatterns` function.

.. code-block:: python

    from django_gears.urls import gears_urlpatterns

    # url definitions here

    urlpatterns += gears_urlpatterns()

Sites using these urlpatterns will not need to use `Django's staticfiles urlpatterns`_.

.. _Django's staticfiles urlpatterns: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/# django.contrib.staticfiles.urls.staticfiles_urlpatterns

.. warning::

    Like staticfiles_urlpatterns, gears_urlpatterns only registers
    patterns when settings.Debug is True. This isn't for production
    use. See the :doc:`Deployment docs <deploying>` for more information.


Gears urlpatterns
-----------------

.. module:: django_gears.urls

.. py:function:: gears_urlpatterns(prefix=None)

    Returns development urlpatterns for serving assets.

    If ``settings.DEBUG`` is false, the returned urlpatterns will be empty.

    :param prefix: The url prefix to server assets under. Defaults to the :setting:`GEARS_URL` setting.
