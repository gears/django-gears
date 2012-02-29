import os
from .settings import *


DEBUG = True
MY_DEBUG = True

INSTALLED_APPS += ('test_serve',)

GEARS_DIRS = (
    os.path.join(TESTS_DIR, 'fixtures', 'serve'),
)
