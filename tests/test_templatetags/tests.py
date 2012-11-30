from mock import patch, Mock

from django.template import Template, Context
from django.test import TestCase

from gears.assets import Asset

class CSSAssetTagTests(TestCase):

    def render(self, code, **context):
        return Template(u'{% load gears %}' + code).render(Context(context))

    def test_outputs_public_asset_in_normal_mode(self):
        self.assertEqual(
            self.render(u'{% css_asset_tag "css/script.css" %}'),
            u'<link rel="stylesheet" href="/static/css/script.css">')

    def test_outputs_all_requirements_in_debug_mode(self):

        with patch.object(Asset, 'mtime') as mtime:
            mtime.__get__ = Mock(return_value = 123)

            self.assertEqual(
                self.render(u'{% css_asset_tag "css/style.css" debug %}'),
                (u'<link rel="stylesheet" href="/static/css/reset.css?body=1&v=123">\n'
                u'<link rel="stylesheet" href="/static/css/base.css?body=1&v=123">\n'
                 u'<link rel="stylesheet" href="/static/css/style.css?body=1&v=123">'))
