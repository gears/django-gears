import warnings

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from django_gears.utils import get_asset_handler
from . import asset_handlers


class GetAssetHandlerTests(TestCase):

    def test_asset_handler_is_a_class(self):
        asset_handler = get_asset_handler('test_get_asset_handler.asset_handlers.PythonCompiler')
        self.assertIs(asset_handler.handler_class, asset_handlers.PythonCompiler)

    def test_asset_handler_class_with_options(self):
        asset_handler = get_asset_handler(
            path='test_get_asset_handler.asset_handlers.CompilerWithOptions',
            options={'level': 9})
        self.assertIs(asset_handler.handler_class, asset_handlers.CompilerWithOptions)

    def test_asset_handler_is_a_callable(self):
        asset_handler = get_asset_handler('test_get_asset_handler.asset_handlers.simple_compiler')
        self.assertIs(asset_handler, asset_handlers.simple_compiler)

    def test_callable_asset_handler_with_options(self):
        with warnings.catch_warnings(record=True) as w:
            get_asset_handler(
                path='test_get_asset_handler.asset_handlers.simple_compiler',
                options={'level': 9})
            self.assertEqual(len(w), 1)
            self.assertIn("{'level': 9} is provided as 'test_get_asset_handler."
                          "asset_handlers.simple_compiler' handler",
                          unicode(w[0].message))

    def test_asset_handler_does_not_exist(self):
        with self.assertRaises(ImproperlyConfigured):
            get_asset_handler('test_get_asset_handler.asset_handlers.nonexistent_handler')

    def test_asset_handler_module_does_not_exist(self):
        with self.assertRaises(ImproperlyConfigured):
            get_asset_handler('test_get_asset_handler.nonexistent_module.handler')

    def test_asset_handler_is_not_a_class_or_callable(self):
        with self.assertRaises(ImproperlyConfigured):
            get_asset_handler('test_get_asset_handler.asset_handlers.incorrect_handler')
