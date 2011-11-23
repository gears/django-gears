from django.conf import settings

GEARS_ROOT = getattr(settings, 'GEARS_ROOT')
GEARS_DIRS = getattr(settings, 'GEARS_DIRS')

GEARS_FINDERS = getattr(settings, 'GEARS_FINDERS', (
    'gears.finders.FileSystemFinder',
))

GEARS_PROCESSORS = getattr(settings, 'GEARS_PROCESSORS', {
    'css': 'gears.processors.CSSProcessor',
    'js': 'gears.processors.JavaScriptProcessor',
})

GEARS_PUBLIC_ASSETS = getattr(settings, 'GEARS_PUBLIC_ASSETS', (
    'css/style.css',
    'js/script.js',
))
