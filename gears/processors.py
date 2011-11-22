from __future__ import with_statement

import os
import re
import shlex

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.utils._os import safe_join

from . import settings


_processors = {}


class InvalidDirective(Exception):
    pass


class BaseProcessor(object):

    def __init__(self, base, path):
        self.base = base
        self.path = path

    def get_absolute_path(self):
        return os.path.join(self.base, self.path)

    def process(self):
        with open(safe_join(self.base, self.path), 'rb') as f:
            return self.process_source(f.read())

    def process_source(self, source):
        raise NotImplementedError()


class RawProcessor(BaseProcessor):

    def process_source(self, source):
        return source


class DirectivesMixin(object):

    extension = None
    header_re = None
    directive_re = None

    def process_source(self, source):
        match = self.header_re.match(source)
        if match:
            header = match.group(0)
            body = self.header_re.sub('', source)
        else:
            header = ''
            body = source
        source = '\n\n'.join(self.process_directives(header, body))
        return source.strip() + '\n'

    def process_directives(self, header, self_body):
        body = []
        directive_linenos = []
        has_require_self = False
        for n, args in self.parse_directives(header):
            try:
                if args[0] == 'require':
                    self.process_require_directive(args[1:], n, body)
                elif args[0] == 'require_self':
                    self.process_require_self_directive(
                        args[1:], n, body, self_body)
                    has_require_self = True
                else:
                    raise InvalidDirective(
                        "%s (%s): unknown directive: %r."
                        % (self.get_absolute_path(), n, args[0]))
            except InvalidDirective:
                pass
            else:
                directive_linenos.append(n)
        if not has_require_self:
            body.append(self_body.strip())
        header = header.splitlines()
        for lineno in reversed(directive_linenos):
            del header[lineno]
        return '\n'.join(header).strip(), '\n\n'.join(body).strip()

    def parse_directives(self, header):
        for n, line in enumerate(header.splitlines()):
            match = self.directive_re.match(line)
            if match:
                yield n, shlex.split(match.group(1))

    def process_require_directive(self, args, lineno, body):
        if len(args) != 1:
            raise InvalidDirective(
                "%s (%s): 'require' directive has wrong number "
                "of arguments (only one argument required): %s."
                % (self.get_absolute_path(), lineno, args))
        path = '%s.%s' % (args[0], self.extension)
        path = os.path.join(os.path.dirname(self.path), path)
        body.append(self.__class__(self.base, path).process().strip())

    def process_require_self_directive(self, args, lineno, body, self_body):
        if args:
            raise InvalidDirective(
                "%s (%s): 'require_self' directive requires no arguments."
                % self.get_absolute_path(), lineno)
        body.append(self_body.strip())


class CSSProcessor(DirectivesMixin, BaseProcessor):

    extension = 'css'
    header_re = re.compile(r'^(\s*/\*.*?\*/)+', re.DOTALL)
    directive_re = re.compile(r"""^\s*\*\s*=\s*(\w+[.'"\s\w-]*)$""")


class JavaScriptProcessor(DirectivesMixin, BaseProcessor):

    extension = 'js'
    header_re = re.compile(r'^(\s*((/\*.*?\*/)|(//[^\n]*\n?)+))+', re.DOTALL)
    directive_re = re.compile(r"""^\s*(?:\*|//)\s*=\s*(\w+[.'"\s\w-]*)$""")


def process(base, path):
    ext = os.path.splitext(path)[1].lstrip('.')
    return get_processor_for_ext(ext)(base, path).process()


def get_processor_for_ext(ext):
    if ext not in settings.GEARS_PROCESSORS:
        return RawProcessor
    return get_processor(settings.GEARS_PROCESSORS[ext])


def _get_processor(processor_path):
    module_name, attr = processor_path.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing module %s: "%s".' % (module, e))
    try:
        Processor = getattr(module, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a "%s" class.' % (module_name, attr))
    if not issubclass(Processor, BaseProcessor):
        raise ImproperlyConfigured(
            'Processor "%s" is not a subclass of "%s".'
            % (Processor, BaseProcessor))
    return Processor
get_processor = memoize(_get_processor, _processors, 1)
