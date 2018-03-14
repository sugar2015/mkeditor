from django import VERSION, forms
from django.template import Context, loader
from django.utils.html import conditional_escape


try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode

class MarkdownWidget(forms.Textarea):


    def __init__(self, *args, **kwargs):
        self.template = "editor.html"
        super(MarkdownWidget, self).__init__(*args, **kwargs)

    @property
    def media(self):
        return forms.Media(
            css={
                "all": ("css/editormd.css","css/style.css")
            },
            js=(
                "js/jquery.min.js",
                "js/editormd.js",
            )
        )

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        if VERSION < (1, 11):
            final_attrs = self.build_attrs(attrs, name=name)
        else:
            final_attrs = self.build_attrs(attrs, {'name': name})
        template = loader.get_template(self.template)
        context = {
            "attrs": flatatt(final_attrs),
            "body": conditional_escape(force_unicode(value)),
        }
        context = Context(context) if VERSION < (1, 9) else context
        return template.render(context)
