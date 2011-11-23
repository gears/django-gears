import mimetypes
import posixpath
import urllib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponse

from .settings import environment


def serve(request, path, document_root=None, insecure=False, **kwargs):
    if not settings.DEBUG and not insecure:
        raise ImproperlyConfigured(
            "The gears view can only be used in debug mode or if the "
            "--insecure option of 'runserver' is used.")
    normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
    if normalized_path in environment.public_assets:
        absolute_path = environment.find(normalized_path)
    else:
        absolute_path = None
    if not absolute_path:
        return staticfiles_serve(request, path, document_root=document_root,
                                 insecure=insecure, **kwargs)
    mimetype, encoding = mimetypes.guess_type(absolute_path)
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(
        environment.process(normalized_path, absolute_path), mimetype=mimetype)
    if encoding:
        response['Content-Encoding'] = encoding
    return response
