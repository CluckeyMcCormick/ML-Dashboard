#Copy pasted code from shymonk
from django import template
from django.template import Context

register = template.Library()


class AjaxTableNode(template.Node):
    template_name = "table/ajax_complex_request_table.html"

    def __init__(self, table, source_name, given_pk):
        self.table = template.Variable(table)
        self.source_name = template.Variable(source_name)
        self.given_pk = template.Variable(given_pk)

    def render(self, context):
        table = self.table.resolve(context)
        source_name = self.source_name.resolve(context)
        given_pk = self.given_pk.resolve(context)

        t = template.loader.get_template(
            table.opts.template_name or self.template_name
        )
        context = {
            'table': table, 
            'source_name' : source_name,
            'given_pk': given_pk,
        }
        return t.render(context)

@register.tag
def render_table_ajax(parser, token):
    try:
        tag, table, source_name, given_pk = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return AjaxTableNode(table, source_name, given_pk)
