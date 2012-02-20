from __future__ import absolute_import
from django.template import Node, Library, TemplateSyntaxError
from gears.assets import build_asset
from ..settings import environment, GEARS_URL, GEARS_DEBUG


register = Library()


class CSSAssetTagNode(Node):

    template = u'<link rel="stylesheet" href="%s%%s">' % GEARS_URL

    def __init__(self, logical_path, debug):
        self.logical_path = logical_path
        self.debug = debug

    def render(self, context):
        logical_path = self.logical_path.resolve(context)
        if self.debug or GEARS_DEBUG:
            asset = build_asset(environment, logical_path)
            paths = (('%s?body=1' % r.attributes.logical_path) for r in asset.requirements)
        else:
            paths = (logical_path,)
        return '\n'.join((self.template % path) for path in paths)


@register.tag
def css_asset_tag(parser, token):
    bits = token.split_contents()
    if len(bits) not in (2, 3):
        raise TemplateSyntaxError("'css_asset_tag' tag takes one argument:"
                                  " the logical path to the public asset")
    debug = (len(bits) == 3)
    if debug and bits[2] != 'debug':
        raise TemplateSyntaxError("Second (optional) argument to"
                                  " 'css_asset_tag' tag must be 'debug'")
    logical_path = parser.compile_filter(bits[1])
    return CSSAssetTagNode(logical_path, debug)
