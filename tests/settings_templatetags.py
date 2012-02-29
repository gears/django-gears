from tests.settings import *


INSTALLED_APPS += ('test_templatetags',)

GEARS_DIRS = (
    os.path.join(TESTS_DIR, 'fixtures', 'templatetags'),
)
