from __future__ import with_statement

import os
from django.test import TestCase
from gears.processors import RawProcessor, CSSProcessor, JavaScriptProcessor


APP_DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(APP_DIR, 'assets')
STATIC_DIR = os.path.join(APP_DIR, 'static')


class RawProcessorTests(TestCase):

    def test_process(self):
        processor = RawProcessor(ASSETS_DIR, 'readme.txt')
        self.assertEqual(processor.process(), 'Read me\n')


class CSSProcessorTests(TestCase):

    def test_directives(self):
        processor = CSSProcessor(ASSETS_DIR, 'css/directives.css')
        with open(os.path.join(STATIC_DIR, 'css', 'directives.css')) as f:
            self.assertEqual(processor.process(), f.read())


class JavaScriptProcessorTests(TestCase):

    def test_directives(self):
        processor = JavaScriptProcessor(ASSETS_DIR, 'js/directives.js')
        with open(os.path.join(STATIC_DIR, 'js', 'directives.js')) as f:
            self.assertEqual(processor.process(), f.read())
