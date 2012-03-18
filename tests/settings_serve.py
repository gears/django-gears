import os
from tests.settings import *


DEBUG = True

INSTALLED_APPS += ('test_serve',)

GEARS_DIRS = (
    os.path.join(TESTS_DIR, 'fixtures', 'serve'),
)
