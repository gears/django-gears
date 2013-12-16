import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.importlib import import_module

from gears.finders import FileSystemFinder


class AppFinder(FileSystemFinder):

    def __init__(self):
        super(AppFinder, self).__init__(self.get_app_assets_dirs())

    def get_app_assets_dirs(self):
        if not six.PY3:
            fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
        app_assets_dirs = []
        for app in settings.INSTALLED_APPS:
            try:
                mod = import_module(app)
            except ImportError as e:
                raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
            assets_dir = os.path.join(os.path.dirname(mod.__file__), 'assets')
            if os.path.isdir(assets_dir):
                if not six.PY3:
                    assets_dir = assets_dir.decode(fs_encoding)
                app_assets_dirs.append(assets_dir)
        app_assets_dirs = tuple(app_assets_dirs)
        return app_assets_dirs
