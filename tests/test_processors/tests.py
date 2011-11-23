from __future__ import with_statement

import os
from django.test import TestCase

from gears.asset_attributes import AssetAttributes
from gears.environment import Environment
from gears.finders import FileSystemFinder
from gears.processors import DirectivesProcessor


APP_DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(APP_DIR, 'assets')
STATIC_DIR = os.path.join(APP_DIR, 'static')


class DirectivesProcessorTests(TestCase):

    def get_environment(self):
        environment = Environment(STATIC_DIR)
        environment.register_defaults()
        environment.finders.register(FileSystemFinder(directories=[ASSETS_DIR]))
        return environment

    def get_processor(self, path):
        environment = self.get_environment()
        absolute_path = os.path.join(ASSETS_DIR, path)
        asset_attributes = AssetAttributes(environment, path, absolute_path)
        return DirectivesProcessor(asset_attributes)

    def test_css_directives(self):
        processor = self.get_processor('css/directives.css')
        with open(os.path.join(STATIC_DIR, 'css', 'directives.css')) as t:
            with open(os.path.join(ASSETS_DIR, 'css', 'directives.css')) as s:
                self.assertEqual(processor.process(s.read()), t.read())

    def test_js_directives(self):
        processor = self.get_processor('js/directives.js')
        with open(os.path.join(STATIC_DIR, 'js', 'directives.js')) as t:
            with open(os.path.join(ASSETS_DIR, 'js', 'directives.js')) as s:
                self.assertEqual(processor.process(s.read()), t.read())
