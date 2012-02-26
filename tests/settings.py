import os


TESTS_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

MEDIA_ROOT = os.path.join(TESTS_DIR, 'public', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(TESTS_DIR, 'public', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(TESTS_DIR, 'static'),
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django_gears',
)

GEARS_ROOT = os.path.join(TESTS_DIR, 'static')
