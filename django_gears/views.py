import mimetypes
import posixpath
import time
import urllib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponse
from django.utils.http import http_date

from gears.assets import build_asset
from gears.compat import bytes
from gears.exceptions import FileNotFound

from .settings import environment

MAX_AGE = 60 * 60 * 24 * 7 # 1 week


def serve(request, path, **kwargs):
    if not settings.DEBUG and not kwargs.get('insecure'):
        raise ImproperlyConfigured(
            "The gears view can only be used in debug mode or if the "
            "--insecure option of 'runserver' is used.")

    # It is only required check because we generate
    # version arg for each file
    if 'HTTP_IF_MODIFIED_SINCE' in request.META:
        response = HttpResponse()
        response['Expires'] = http_date(time.time() + MAX_AGE)
        response.status_code = 304
        return response

    normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
    try:
        asset = build_asset(environment, normalized_path)
    except FileNotFound:
        return staticfiles_serve(request, path, **kwargs)

    last_modified = asset.mtime
    if request.GET.get('body'):
        asset = asset.processed_source
    mimetype, encoding = mimetypes.guess_type(normalized_path)
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(bytes(asset), mimetype=mimetype)
    if encoding:
        response['Content-Encoding'] = encoding
    response['Last-Modified'] = http_date(last_modified)
    return response
