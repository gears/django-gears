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

    def get_processor(self):
        format_extension = self.get_format_extension()
        processor_class = self.environment.processors.get(format_extension)
        return processor_class(self)
