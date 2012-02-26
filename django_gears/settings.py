from django.conf import settings
from gears.environment import Environment
from .utils import (get_compiler_class, get_finder_class, get_processor_class,
                    get_compressor_class)


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

DEFAULT_PUBLIC_ASSETS = (
    'css/style.css',
    'js/script.js',
)

GEARS_DEBUG = getattr(settings, 'GEARS_DEBUG', settings.DEBUG)

GEARS_URL = getattr(settings, 'GEARS_URL', settings.STATIC_URL)


environment = Environment(getattr(settings, 'GEARS_ROOT'))
environment.compilers.register_defaults()

for finder_class in getattr(settings, 'GEARS_FINDERS', DEFAULT_FINDERS):
    if isinstance(finder_class, (list, tuple)):
        finder_class, options = finder_class
    else:
        options = {}
    finder_class = get_finder_class(finder_class)
    environment.finders.register(finder_class(**options))

mimetypes = getattr(settings, 'GEARS_MIMETYPES', DEFAULT_MIMETYPES)
for extension, mimetype in mimetypes.items():
    environment.mimetypes.register(extension, mimetype)

for extension, compiler_class in getattr(settings, 'GEARS_COMPILERS', {}).items():
    if isinstance(compiler_class, (list, tuple)):
        compiler_class, options = compiler_class
    else:
        options = {}
    compiler_class = get_compiler_class(compiler_class)
    environment.compilers.register(extension, compiler_class.as_handler(**options))

public_assets = getattr(settings, 'GEARS_PUBLIC_ASSETS', DEFAULT_PUBLIC_ASSETS)
for public_asset in public_assets:
    environment.public_assets.register(public_asset)

preprocessors = getattr(settings, 'GEARS_PREPROCESSORS', DEFAULT_PREPROCESSORS)
for mimetype, preprocessor_classes in preprocessors.items():
    if not isinstance(preprocessor_classes, (list, tuple)):
        preprocessor_classes = [preprocessor_classes]
    for preprocessor_class in preprocessor_classes:
        preprocessor_class = get_processor_class(preprocessor_class)
        environment.preprocessors.register(mimetype, preprocessor_class.as_handler())

postprocessors = getattr(settings, 'GEARS_POSTPROCESSORS', {})
for mimetype, postprocessor_classes in postprocessors.items():
    if not isinstance(postprocessor_classes, (list, tuple)):
        postprocessor_classes = [postprocessor_classes]
    for postprocessor_class in postprocessor_classes:
        postprocessor_class = get_processor_class(postprocessor_class)
        environment.postprocessors.register(mimetype, postprocessor_class.as_handler())

compressors = getattr(settings, 'GEARS_COMPRESSORS', {})
for mimetype, compressor_class in compressors.items():
    compressor_class = get_compressor_class(compressor_class)
    environment.compressors.register(mimetype, compressor_class.as_handler())
