from .processors import DirectivesProcessor


class Finders(list):

    def register(self, finder):
        if finder not in self:
            self.append(finder)

    def unregister(self, finder):
        if finder in self:
            self.remove(finder)


class Processors(dict):

    def register_defaults(self):
        self.register('.css', DirectivesProcessor)
        self.register('.js', DirectivesProcessor)

    def register(self, extension, processor_class):
        self[extension] = processor_class

    def unregister(self, extension):
        if extension in self:
            del self[extension]

    def get(self, extension):
        return super(Processors, self).get(extension)


class PublicAssets(list):

    def register_defaults(self):
        self.register('css/style.css')
        self.register('js/script.js')

    def register(self, path):
        if path not in self:
            self.append(path)

    def unregister(self, path):
        if path in self:
            self.remove(path)


class Environment(object):

    def __init__(self, root):
        self.root = root
        self.finders = Finders()
        self.processors = Processors()
        self.public_assets = PublicAssets()

    def register_defaults(self):
        self.processors.register_defaults()
        self.public_assets.register_defaults()

    def find(self, path, all=False):
        matches = []
        for finder in self.finders:
            result = finder.find(path, all=all)
            if not all and result:
                return result
            if not isinstance(result, (list, tuple)):
                result = []
            matches.extend(result)
        if matches:
            return matches
        return [] if all else None
