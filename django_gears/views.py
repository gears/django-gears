import mimetypes
import posixpath
import urllib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponse

from gears.assets import build_asset
from gears.exceptions import FileNotFound

from .settings import environment


def serve(request, path, **kwargs):
    if not settings.DEBUG and not kwargs.get('insecure'):
        raise ImproperlyConfigured(
            "The gears view can only be used in debug mode or if the "
            "--insecure option of 'runserver' is used.")
    normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
    try:
        asset = build_asset(environment, normalized_path)
    except FileNotFound:
        return staticfiles_serve(request, path, **kwargs)
    if request.GET.get('body'):
        asset = asset.processed_source
    mimetype, encoding = mimetypes.guess_type(normalized_path)
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(unicode(asset), mimetype=mimetype)
    if encoding:
        response['Content-Encoding'] = encoding
    return response
