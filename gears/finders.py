import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.utils._os import safe_join


_finder_classes = {}


class BaseFinder(object):

    def find(self, path, all=False):
        raise NotImplementedError()


class FileSystemFinder(BaseFinder):

    def __init__(self, directories):
        self.locations = []
        if not isinstance(directories, (list, tuple)):
            raise ImproperlyConfigured(
                "FileSystemFinder's 'directories' parameter is not a "
                "tuple or list; perhaps you forgot a trailing comma?")
        for directory in directories:
            if directory not in self.locations:
                self.locations.append(directory)

    def find(self, path, all=False):
        matches = []
        for root in self.locations:
            matched_path = self.find_location(root, path)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, path):
        path = safe_join(root, path)
        if os.path.exists(path):
            return path


def _get_finder_class(path):
    module_name, attr = path.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing module %s: "%s".' % (module, e))
    try:
        Finder = getattr(module, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a "%s" class.' % (module_name, attr))
    if not issubclass(Finder, BaseFinder):
        raise ImproperlyConfigured(
            'Finder "%s" is not a subclass of "%s".' % (Finder, BaseFinder))
    return Finder
get_finder_class = memoize(_get_finder_class, _finder_classes, 1)
