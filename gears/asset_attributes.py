import os
import re


class AssetAttributes(object):

    def __init__(self, environment, path, absolute_path):
        self.environment = environment
        self.path = path
        self.absolute_path = absolute_path

    def get_extensions(self):
        return re.findall(r'\.[^.]+', os.path.basename(self.path))

    def get_format_extension(self):
        extensions = self.get_extensions()
        if extensions:
            return extensions[-1]

    def get_processors(self):
        mimetype = self.get_mimetype()
        processor_classes = self.environment.processors.get(mimetype)
        return [cls(self) for cls in processor_classes]

    def get_mimetype(self):
        return (self.environment.mimetypes.get(self.get_format_extension()) or
                'application/octet-stream')
