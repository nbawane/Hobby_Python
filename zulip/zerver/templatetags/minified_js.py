from __future__ import absolute_import
from typing import Any, Dict

from django.template import Node, Library, TemplateSyntaxError
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

if False:
    # no need to add dependency
    from django.template.base import Parser, Token

register = Library()

class MinifiedJSNode(Node):
    def __init__(self, sourcefile):
        # type: (str) -> None
        self.sourcefile = sourcefile

    def render(self, context):
        # type: (Dict[str, Any]) -> str
        if settings.DEBUG:
            source_files = settings.JS_SPECS[self.sourcefile]
            normal_source = source_files['source_filenames']
            minified_source = source_files.get('minifed_source_filenames', [])

            # Minified source files (most likely libraries) should be loaded
            # first to prevent any dependency errors.
            scripts = minified_source + normal_source
        else:
            scripts = [settings.JS_SPECS[self.sourcefile]['output_filename']]
        script_urls = [staticfiles_storage.url(script) for script in scripts]
        script_tags = ['<script type="text/javascript" src="%s" charset="utf-8"></script>'
                       % url for url in script_urls]
        return '\n'.join(script_tags)


@register.tag
def minified_js(parser, token):
    # type: (Parser, Token) -> MinifiedJSNode
    try:
        tag_name, sourcefile = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%s tag requires an argument" % (tag_name,))
    if not (sourcefile[0] == sourcefile[-1] and sourcefile[0] in ('"', "'")):
        raise TemplateSyntaxError("%s tag should be quoted" % (tag_name,))

    sourcefile = sourcefile[1:-1]
    if sourcefile not in settings.JS_SPECS:
        raise TemplateSyntaxError("%s tag invalid argument: no JS file %s"
                                  % (tag_name, sourcefile))
    return MinifiedJSNode(sourcefile)
