from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django_gears.utils import get_finder
from . import finders


class GetFinderTests(TestCase):

    def test_if_it_is_a_subclass_of_base_finder(self):
        finder = get_finder('test_get_finder.finders.GoodFinder')
        self.assertIsInstance(finder, finders.GoodFinder)

    def test_if_it_is_not_a_subclass_of_base_finder(self):
        with self.assertRaises(ImproperlyConfigured):
            get_finder('test_get_finder.finders.BadFinder')
