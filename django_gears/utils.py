import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from gears.engines.base import BaseEngine
from gears.finders import BaseFinder
from gears.processors import BaseProcessor


_engine_classes = {}
_finder_classes = {}
_processor_classes = {}


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


def get_engine_class(path):
    return get_class(path, _engine_classes, BaseEngine)


def get_finder_class(path):
    return get_class(path, _finder_classes, BaseFinder)


def get_processor_class(path):
    return get_class(path, _processor_classes, BaseProcessor)
