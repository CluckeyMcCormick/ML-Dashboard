from django.utils.safestring import mark_safe

from table.utils import Accessor, A
from table.columns import Column, LinkColumn, DatetimeColumn, Link

class BooleanIconColumn(Column):
    def __init__(self, field=None, header=None, true_icon=None, false_icon=None, true_class='', false_class='', **kwargs):
        super(BooleanIconColumn, self).__init__(field=field, header=header, **kwargs)
        self.true_icon = true_icon
        self.false_icon = false_icon

        self.true_class = true_class
        self.false_class = false_class

    def render(self, obj):
        checked = bool(Accessor(self.field).resolve(obj)) if self.field else False

        safe_str = mark_safe('')

        general_string = '<span class="glyphicon {0} {1}" aria-hidden="true"></span>'

        if checked and (self.true_icon is not None):
            safe_str = mark_safe( general_string.format(self.true_icon, self.true_class) )
        elif (not checked) and (self.false_icon is not None):
            safe_str = mark_safe( general_string.format(self.false_icon, self.false_class) )

        return safe_str

class CheckOnlyColumn(BooleanIconColumn):
    def __init__(self, field=None, header=None, true_class='', **kwargs):
        super(CheckOnlyColumn, self).__init__(field=field, header=header, true_icon='glyphicon-ok', true_class=true_class, **kwargs)

class CustomNoneColumn(Column):
    def __init__(self, field=None, header=None, none_str='', **kwargs):
        super(CustomNoneColumn, self).__init__(field=field, header=header, **kwargs)
        self.none_str = none_str

    def render(self, obj):
        ret = ''
        if Accessor(self.field).resolve(obj):
            ret = super(CustomNoneColumn, self).render(obj)
        else:
            ret = mark_safe(self.none_str)

        return ret

class NoneableDatetimeColumn(DatetimeColumn):
    def render(self, obj):
        ret = mark_safe('')
        if Accessor(self.field).resolve(obj):
            ret = super(NoneableDatetimeColumn, self).render(obj)

        return ret

class TagColumn(Column):
    def __init__(self, field=None, header=None, wrap_class='', **kwargs):
        super(TagColumn, self).__init__(field=field, header=header, **kwargs)
        self.wrap_class = wrap_class

    def render(self, obj):
        output_form = '<strong class="{0} {1}">{2}</strong>'
        val = super(TagColumn, self).render(obj)

        return mark_safe( output_form.format(self.wrap_class, val.lower(), val) )
        