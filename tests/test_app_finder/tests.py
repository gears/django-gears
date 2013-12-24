from __future__ import with_statement

import codecs
import os

from django.conf import settings
from django.test import TestCase, RequestFactory
from django.utils.encoding import smart_str

from django_gears.finders import AppFinder
from django_gears.views import serve


TESTS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')
APP_ASSETS= os.path.join(os.path.dirname(__file__), 'assets')


def read(file):
    with codecs.open(file, encoding='utf-8') as f:
        return f.read()


class AppFinderTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.old_DEBUG = settings.DEBUG
        settings.DEBUG = True

    def tearDown(self):
        settings.DEBUG = self.old_DEBUG

    def get_response(self, path, data=None):
        request = self.factory.get('/static/' + path, data or {})
        return serve(request, path)

    def get_app_asset(self, path):
        return smart_str(read(os.path.join(APP_ASSETS, path)), 'utf-8')

    def test_finder(self):
        finder = AppFinder()
        self.assertItemsEqual(finder.list('js'), (
            ('js/test_app_finder.js', os.path.join(APP_ASSETS, 'js', 'test_app_finder.js')),
        ))

    def test_serve(self):
        response = self.get_response('js/test_app_finder.js')
        self.assertEqual(response.content, self.get_app_asset('js/test_app_finder.js'))
