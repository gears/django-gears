from __future__ import with_statement

import os
import re
import shlex

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module

from .asset_attributes import AssetAttributes
from .assets import Asset


_processor_classes = {}


class InvalidDirective(Exception):
    pass


class BaseProcessor(object):

    def __init__(self, asset_attributes):
        self.asset_attributes = asset_attributes
        self.environment = asset_attributes.environment
        self.path = asset_attributes.path
        self.absolute_path = asset_attributes.absolute_path

    def process(self, source):
        raise NotImplementedError()


class DirectivesProcessor(BaseProcessor):

    header_re = re.compile(r'^(\s*((/\*.*?\*/)|(//[^\n]*\n?)+))+', re.DOTALL)
    directive_re = re.compile(r"""^\s*(?:\*|//)\s*=\s*(\w+[.'"\s\w-]*)$""")

    def process(self, source):
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
        for lineno, args in self.parse_directives(header):
            try:
                if args[0] == 'require':
                    self.process_require_directive(args[1:], lineno, body)
                elif args[0] == 'require_self':
                    self.process_require_self_directive(
                        args[1:], lineno, body, self_body)
                    has_require_self = True
                else:
                    raise InvalidDirective(
                        "%s (%s): unknown directive: %r."
                        % (self.absolute_path, lineno, args[0]))
            except InvalidDirective:
                pass
            else:
                directive_linenos.append(lineno)
        if not has_require_self:
            body.append(self_body.strip())
        header = self.strip_header(header, directive_linenos)
        return header, '\n\n'.join(body).strip()

    def strip_header(self, header, linenos):
        header = header.splitlines()
        for lineno in reversed(linenos):
            del header[lineno]
        return '\n'.join(header).strip()

    def parse_directives(self, header):
        for lineno, line in enumerate(header.splitlines()):
            match = self.directive_re.match(line)
            if match:
                yield lineno, shlex.split(match.group(1))

    def process_require_directive(self, args, lineno, body):
        if len(args) != 1:
            raise InvalidDirective(
                "%s (%s): 'require' directive has wrong number "
                "of arguments (only one argument required): %s."
                % (self.absolute_path, lineno, args))
        path = args[0] + self.asset_attributes.get_format_extension()
        path = os.path.join(os.path.dirname(self.path), path)
        absolute_path = self.environment.find(path)
        if not absolute_path:
            raise InvalidDirective(
                "%s (%s): required file does not exist."
                % (self.absolute_path, lineno))
        asset_attributes = AssetAttributes(
            self.environment, path, absolute_path)
        body.append(str(Asset(asset_attributes)).strip())

    def process_require_self_directive(self, args, lineno, body, self_body):
        if args:
            raise InvalidDirective(
                "%s (%s): 'require_self' directive requires no arguments."
                % self.absolute_path, lineno)
        body.append(self_body.strip())


def _get_processor_class(path):
    module_name, attr = path.rsplit('.', 1)
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
get_processor_class = memoize(_get_processor_class, _processor_classes, 1)
