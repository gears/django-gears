import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.utils._os import safe_join

from . import settings


_finders = SortedDict()


class BaseFinder(object):

    def find(self, path, all=False):
        raise NotImplementedError()


class FileSystemFinder(BaseFinder):

    def __init__(self):
        self.locations = []
        if not isinstance(settings.GEARS_DIRS, (list, tuple)):
            raise ImproperlyConfigured(
                'Your GEARS_DIRS setting is not a tuple or list; '
                'perhaps you forgot a trailing comma?')
        for root in settings.GEARS_DIRS:
            if os.path.abspath(root) == os.path.abspath(settings.GEARS_ROOT):
                raise ImproperlyConfigured(
                    'The GEARS_DIRS setting should not contain the '
                    'GEARS_ROOT setting')
            if root not in self.locations:
                self.locations.append(root)

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
        if path not in settings.GEARS_ASSETS:
            return
        path = safe_join(root, path)
        if os.path.exists(path):
            return path


def find(path, all=False):
    matches = []
    for finder in get_finders():
        result = finder.find(path, all=all)
        if not all and result:
            return result
        if not isinstance(result, (list, tuple)):
            result = [result]
        matches.extend(result)
    if matches:
        return matches
    return [] if all else None


def get_finders():
    for finder_path in settings.GEARS_FINDERS:
        yield get_finder(finder_path)


def _get_finder(finder_path):
    module_name, attr = finder_path.rsplit('.', 1)
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
    return Finder()
get_finder = memoize(_get_finder, _finders, 1)
