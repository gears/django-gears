from django.conf import settings
from gears.environment import Environment, DEFAULT_PUBLIC_ASSETS
from .utils import get_cache, get_finder, get_asset_handler


DEFAULT_CACHE = 'gears.cache.SimpleCache'

DEFAULT_FINDERS = (
    ('gears.finders.FileSystemFinder', {
        'directories': getattr(settings, 'GEARS_DIRS', ()),
    }),
)

DEFAULT_MIMETYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript',
}

DEFAULT_PREPROCESSORS = {
    'text/css': 'gears.processors.DirectivesProcessor',
    'application/javascript': 'gears.processors.DirectivesProcessor',
}

GEARS_DEBUG = getattr(settings, 'GEARS_DEBUG', settings.DEBUG)

GEARS_URL = getattr(settings, 'GEARS_URL', settings.STATIC_URL)


path = getattr(settings, 'GEARS_CACHE', DEFAULT_CACHE)
if isinstance(path, (list, tuple)):
    path, options = path
else:
    options = None
cache = get_cache(path, options)

environment = Environment(
    root=getattr(settings, 'GEARS_ROOT'),
    public_assets=getattr(settings, 'GEARS_PUBLIC_ASSETS', DEFAULT_PUBLIC_ASSETS),
    cache=cache,
)

for path in getattr(settings, 'GEARS_FINDERS', DEFAULT_FINDERS):
    if isinstance(path, (list, tuple)):
        path, options = path
    else:
        options = None
    environment.finders.register(get_finder(path, options))

mimetypes = getattr(settings, 'GEARS_MIMETYPES', DEFAULT_MIMETYPES)
for extension, mimetype in mimetypes.items():
    environment.mimetypes.register(extension, mimetype)

for extension, path in getattr(settings, 'GEARS_COMPILERS', {}).items():
    if isinstance(path, (list, tuple)):
        path, options = path
    else:
        options = {}
    environment.compilers.register(extension, get_asset_handler(path, options))

preprocessors = getattr(settings, 'GEARS_PREPROCESSORS', DEFAULT_PREPROCESSORS)
for mimetype, paths in preprocessors.items():
    if not isinstance(paths, (list, tuple)):
        paths = [paths]
    for path in paths:
        environment.preprocessors.register(mimetype, get_asset_handler(path))

postprocessors = getattr(settings, 'GEARS_POSTPROCESSORS', {})
for mimetype, paths in postprocessors.items():
    if not isinstance(paths, (list, tuple)):
        paths = [paths]
    for path in paths:
        environment.postprocessors.register(mimetype, get_asset_handler(path))

compressors = getattr(settings, 'GEARS_COMPRESSORS', {})
for mimetype, path in compressors.items():
    environment.compressors.register(mimetype, get_asset_handler(path))
