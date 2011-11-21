import mimetypes
import os
import posixpath
import urllib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponse

from . import finders
from . import processors


def serve(request, path, document_root=None, insecure=False, **kwargs):
    if not settings.DEBUG and not insecure:
        raise ImproperlyConfigured(
            "The gears view can only be used in debug mode or if the "
            "--insecure option of 'runserver' is used.")
    normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
    absolute_path = finders.find(normalized_path)
    if not absolute_path:
        return staticfiles_serve(request, path, document_root=document_root,
                                 insecure=insecure, **kwargs)
    document_root, path = os.path.split(absolute_path)
    mimetype, encoding = mimetypes.guess_type(absolute_path)
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(
        processors.process(document_root, path), mimetype=mimetype)
    if encoding:
        response['Content-Encoding'] = encoding
    return response
