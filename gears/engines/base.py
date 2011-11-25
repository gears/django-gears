from subprocess import Popen, PIPE

from django.utils.importlib import import_module
from ..exceptions import ImproperlyConfigured


_engine_classes = {}


class EngineProcessFailed(Exception):
    pass


class BaseEngine(object):

    result_mimetype = None

    def process(self, source, context, calls):
        raise NotImplementedError()


class ExecEngine(BaseEngine):

    params = []

    def __init__(self, executable):
        self.executable = executable

    def process(self, source, context, calls):
        args = [self.executable] + self.params
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, errors = p.communicate(input=source)
        if p.returncode == 0:
            return output
        raise EngineProcessFailed(errors)


def get_engine_class(path):
    if path in _engine_classes:
        return _engine_classes[path]
    module_name, attr = path.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing module %s: "%s".' % (module, e))
    try:
        Engine = getattr(module, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a "%s" class.' % (module_name, attr))
    if not issubclass(Engine, BaseEngine):
        raise ImproperlyConfigured(
            'Engine "%s" is not a subclass of "%s".' % (Engine, BaseEngine))
    _engine_classes[path] = Engine
    return Engine
