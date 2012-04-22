import warnings

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from gears.asset_handler import BaseAssetHandler
from gears.finders import BaseFinder


_cache = {}


def _get_module(path):
    try:
        return import_module(path)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s".' % (path, e))


def _get_module_attr(module_path, name):
    try:
        return getattr(_get_module(module_path), name)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" obj.' % (module_path, name))


def _get_object(path):
    if path not in _cache:
        _cache[path] = _get_module_attr(*path.rsplit('.', 1))
    return _cache[path]


def get_cache(path, options=None):
    cls = _get_object(path)
    return cls(**(options or {}))


def get_finder(path, options=None):
    cls = _get_object(path)
    if not issubclass(cls, BaseFinder):
        raise ImproperlyConfigured('"%s" is not a subclass of BaseFinder.' % path)
    return cls(**(options or {}))


def get_asset_handler(path, options=None):
    obj = _get_object(path)
    try:
        if issubclass(obj, BaseAssetHandler):
            return obj.as_handler(**(options or {}))
    except TypeError:
        pass
    if callable(obj):
        if options is not None:
            warnings.warn('%r is provided as %r handler options, but not used '
                'because this handler is not a BaseAssethandler subclass.'
                % (options, path))
        return obj
    raise ImproperlyConfigured('"%s" must be a BaseAssetHandler subclass or callable object' % path)
