from __future__ import with_statement

import codecs
import os

from django.conf import settings
from django.test import TestCase, RequestFactory
from django.utils.encoding import smart_str

from django_gears.views import serve


TESTS_DIR = os.path.join(os.path.dirname(__file__), '..')
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures', 'serve')


def read(file):
    with codecs.open(file, encoding='utf-8') as f:
        return f.read()


class ServeViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.old_DEBUG = settings.DEBUG
        settings.DEBUG = True

    def tearDown(self):
        settings.DEBUG = self.old_DEBUG

    def get_response(self, path, data=None):
        request = self.factory.get('/static/' + path, data or {})
        return serve(request, path)

    def get_fixture(self, path):
        return smart_str(read(os.path.join(FIXTURES_DIR, path)), 'utf-8')

    def test_returns_asset(self):
        response = self.get_response('js/script.js')
        self.assertEqual(response.content, self.get_fixture('output.js'))

    def test_returns_processed_source_if_body_requested(self):
        response = self.get_response('js/script.js', {'body': 1})
        self.assertEqual(response.content, self.get_fixture('output_body.js'))
