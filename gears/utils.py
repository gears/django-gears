from django.utils.importlib import import_module
from .exceptions import ImproperlyConfigured


missing = object()


class cached_property(object):

    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, missing)
        if value is missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value


def first(function, iterable):
    if function is None:
        function = bool
    for item in iterable:
        if function(item):
            return item
    raise ValueError('No suitable value found.')


def first_or_none(function, iterable):
    try:
        return first(function, iterable)
    except ValueError:
        pass


def get_class(path, cache, base_class=None):
    if path in cache:
        return cache[path]
    module_name, attr = path.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing module %s: "%s".' % (module, e))
    try:
        cls = getattr(module, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a "%s" class.' % (module_name, attr))
    if base_class is not None and not issubclass(cls, base_class):
        raise ImproperlyConfigured(
            '"%s" is not a subclass of "%s".' % (cls, base_class))
    cache[path] = cls
    return cls


_engine_classes = {}
_finder_classes = {}
_processor_classes = {}


def get_engine_class(path):
    from .engines.base import BaseEngine
    return get_class(path, _engine_classes, BaseEngine)


def get_finder_class(path):
    from .finders import BaseFinder
    return get_class(path, _finder_classes, BaseFinder)


def get_processor_class(path):
    from .processors import BaseProcessor
    return get_class(path, _processor_classes, BaseProcessor)
