import os
import re


class AssetAttributes(object):

    def __init__(self, environment, path):
        self.environment = environment
        self.path = path

    def get_search_paths(self):
        paths = [self.path]
        path_without_extensions = self.get_path_without_extensions()
        if os.path.basename(path_without_extensions) != 'index':
            path = os.path.join(path_without_extensions, 'index')
            path += ''.join(self.get_extensions())
            paths.append(path)
        return paths

    def get_path_without_extensions(self):
        suffix = ''.join(self.get_extensions())
        if suffix:
            return self.path[:-len(suffix)]
        return self.path

    def get_extensions(self):
        return re.findall(r'\.[^.]+', os.path.basename(self.path))

    def get_format_extension(self):
        for extension in self.get_extensions():
            engine = self.environment.engines.get(extension)
            if not engine and self.environment.mimetypes.get(extension):
                return extension

    def get_suffix(self):
        extensions = self.get_extensions()
        try:
            index = extensions.index(self.get_format_extension())
        except ValueError:
            return extensions
        return extensions[index:]

    def get_engine_extensions(self):
        return [e for e in self.get_suffix()[1:]
                if self.environment.engines.get(e)]

    def get_engines(self):
        return [self.environment.engines.get(e)
                for e in self.get_engine_extensions()]

    def get_processors(self):
        mimetype = self.get_mimetype()
        processor_classes = self.environment.processors.get(mimetype)
        processors = [cls(self) for cls in processor_classes]
        processors.extend(reversed(self.get_engines()))
        return processors

    def get_mimetype(self):
        return (self.environment.mimetypes.get(self.get_format_extension()) or
                'application/octet-stream')
