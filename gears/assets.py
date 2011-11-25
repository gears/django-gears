from __future__ import with_statement


class AssetAlreadyUsed(Exception):
    pass


class BaseAsset(object):

    def __init__(self, attributes, absolute_path, calls=None):
        self.attributes = attributes
        self.absolute_path = absolute_path
        self.calls = calls or set()
        if self.absolute_path in self.calls:
            raise AssetAlreadyUsed(
                'Asset %r already used earlier.' % absolute_path)
        self.calls.add(self.absolute_path)

    def get_source(self):
        raise NotImplementedError()

    def __str__(self):
        return self.get_source()


class Asset(BaseAsset):

    def get_source(self):
        with open(self.absolute_path, 'rb') as f:
            source = f.read()
        for processor in self.attributes.processors:
            source = processor.process(source, self.calls)
        return source


class StaticAsset(BaseAsset):

    def get_source(self):
        with open(self.absolute_path, 'rb') as f:
            return f.read()
