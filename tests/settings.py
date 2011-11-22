import os


TESTS_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TESTS_DIR, 'sqlite.db'),
    }
}

MEDIA_ROOT = os.path.join(TESTS_DIR, 'public', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(TESTS_DIR, 'public', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(TESTS_DIR, 'static'),
)

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'gears',
    'tests.test_processors',
)

GEARS_ROOT = os.path.join(TESTS_DIR, 'static')

GEARS_DIRS = (
    os.path.join(TESTS_DIR, 'assets'),
)
