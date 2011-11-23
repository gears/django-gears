from __future__ import with_statement

import os
from django.test import TestCase

from gears.environment import Environment
from gears.finders import FileSystemFinder
from gears.processors import RawProcessor, CSSProcessor, JavaScriptProcessor


APP_DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(APP_DIR, 'assets')
STATIC_DIR = os.path.join(APP_DIR, 'static')


class ProcessorTests(TestCase):

    processor_class = None

    def get_environment(self):
        environment = Environment(STATIC_DIR)
        environment.finders.register(FileSystemFinder(directories=[ASSETS_DIR]))
        return environment

    def get_processor(self, path):
        environment = self.get_environment()
        absolute_path = os.path.join(ASSETS_DIR, path)
        return self.processor_class(environment, path, absolute_path)


class RawProcessorTests(ProcessorTests):

    processor_class = RawProcessor

    def test_process(self):
        processor = self.get_processor('readme.txt')
        self.assertEqual(processor.process(), 'Read me\n')


class CSSProcessorTests(ProcessorTests):

    processor_class = CSSProcessor

    def test_directives(self):
        processor = self.get_processor('css/directives.css')
        with open(os.path.join(STATIC_DIR, 'css', 'directives.css')) as f:
            self.assertEqual(processor.process(), f.read())


class JavaScriptProcessorTests(ProcessorTests):

    processor_class = JavaScriptProcessor

    def test_directives(self):
        processor = self.get_processor('js/directives.js')
        with open(os.path.join(STATIC_DIR, 'js', 'directives.js')) as f:
            self.assertEqual(processor.process(), f.read())
