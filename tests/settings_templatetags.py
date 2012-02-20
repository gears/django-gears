from .settings import *


INSTALLED_APPS += ('tests.test_templatetags',)

GEARS_DIRS = (
    os.path.join(TESTS_DIR, 'fixtures', 'templatetags'),
)
