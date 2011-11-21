from __future__ import with_statement

import os
import re

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.utils._os import safe_join

from . import settings


_processors = {}


class BaseProcessor(object):

    def __init__(self, base, path):
        self.base = base
        self.path = path

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
        match = re.match(self.header_re, source, re.DOTALL)
        if match:
            header = match.group(0)
            body = re.sub(self.header_re, '', source, flags=re.DOTALL)
        else:
            header = ''
            body = source
        return '\n'.join(self.process_directives(header, body))

    def process_directives(self, header, self_body):
        body = []
        directive_linenos = []
        for n, name, path in self.parse_directives(header):
            path = '.'.join((path, self.extension))
            processor = self.__class__(self.base, path)
            body.append(processor.process())
            directive_linenos.append(n)
        body.append(self_body)
        header = header.splitlines()
        for lineno in reversed(directive_linenos):
            del header[lineno]
        return '\n'.join(header), '\n'.join(body)

    def parse_directives(self, header):
        for n, line in enumerate(header.splitlines()):
            match = re.match(self.directive_re, line)
            if match:
                yield n, match.group(1), match.group(2)


class CSSProcessor(DirectivesMixin, BaseProcessor):

    extension = 'css'
    header_re = r'^(\s*/\*.*?\*/)+'
    directive_re = r'^\s*\*=\s+(require)\s+(.*)$'


class JavaScriptProcessor(DirectivesMixin, BaseProcessor):

    extension = 'js'
    header_re = r'^(\s*((/\*.*?\*/)|(//[^\n]*\n?)+))+'
    directive_re = r'^\s*(?:\*|//)=\s+(require)\s+(.*)$'


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
