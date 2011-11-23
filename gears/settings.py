from django.conf import settings

from .environment import Environment
from .finders import get_finder_class
from .processors import get_processor_class


DEFAULT_FINDERS = (
    ('gears.finders.FileSystemFinder', {
        'directories': getattr(settings, 'GEARS_DIRS', ()),
    }),
)

DEFAULT_PROCESSORS = {
    '.css': 'gears.processors.DirectivesProcessor',
    '.js': 'gears.processors.DirectivesProcessor',
}

DEFAULT_PUBLIC_ASSETS = (
    'css/style.css',
    'js/script.js',
)


environment = Environment(getattr(settings, 'GEARS_ROOT'))

for finder_class in getattr(settings, 'GEARS_FINDERS', DEFAULT_FINDERS):
    if isinstance(finder_class, (list, tuple)):
        finder_class, options = finder_class
    else:
        options = {}
    finder_class = get_finder_class(finder_class)
    environment.finders.register(finder_class(**options))

processors = getattr(settings, 'GEARS_PROCESSORS', DEFAULT_PROCESSORS)
for extension, processor_classes in processors.items():
    if not isinstance(processor_classes, (list, tuple)):
        processor_classes = [processor_classes]
    for processor_class in processor_classes:
        processor_class = get_processor_class(processor_class)
        environment.processors.register(extension, processor_class)

public_assets = getattr(settings, 'GEARS_PUBLIC_ASSETS', DEFAULT_PUBLIC_ASSETS)
for public_asset in public_assets:
    environment.public_assets.register(public_asset)
