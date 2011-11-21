from django.contrib.staticfiles.handlers import StaticFilesHandler
from .views import serve


class AssetFilesHandler(StaticFilesHandler):

    def serve(self, request):
        return serve(request, self.file_path(request.path), insecure=True)
