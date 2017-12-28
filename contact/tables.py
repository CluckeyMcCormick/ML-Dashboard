from django.utils.safestring import mark_safe

from table import Table
from table.utils import Accessor, A
from table.columns import Column, LinkColumn, DatetimeColumn, Link

from .models import ContactTypeTag, Task, TaskContactAssoc
from .models import Organization, Contact, Project

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

        print(Accessor(self.field).resolve(obj))

        return mark_safe( output_form.format(self.wrap_class, val.lower(), val) )
        
        
gen_attrs = {'class': 'centerized'}

class ContactTable(Table):
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='contact-detail', 
                args=(
                    A('id'),
                ),
                attrs={
                    'class':
                        'glyphicon glyphicon-eye-open'
                },
            ),
        ],
        searchable=False,
        sortable=False,
    )

    name = Column(field='name', header='Name')
    email = Column(field='email', header='E-Mail')
    phone = Column(field='phone', header='Phone')
    tags = Column(field='type_list_string', visible=False)

    is_volunteer = CheckOnlyColumn(
        field='is_volunteer', header='Volunteer', 
        true_class='contag icon vo', 
        attrs=gen_attrs,)

    is_prospect = CheckOnlyColumn(
        field='is_prospect', header='Prospect', 
        true_class='contag icon pr', 
        attrs=gen_attrs,)

    is_donor = CheckOnlyColumn(
        field='is_donor', header='Donor', 
        true_class='contag icon do', 
        attrs=gen_attrs,)

    is_resource = CheckOnlyColumn(
        field='is_resource', header='Resource', 
        true_class='contag icon _g', 
        attrs=gen_attrs,)

    is_foundation = CheckOnlyColumn(
        field='is_foundation', header='Foundation', 
        true_class='contag icon _f', 
        attrs=gen_attrs,)

    class Meta:
        model = Contact
        search = True

        attrs = {'class': 'table-striped table-hover'}

class TaskTable(Table):
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='task-detail', 
                args=(
                    A('id'),
                ),
                attrs={
                    'class':
                        'glyphicon glyphicon-eye-open'
                },
            ),
        ],
        searchable=False,
        sortable=False,
    )

    brief = Column(field='brief', header='Brief')
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format='%b %d, %Y')
    status = TagColumn(field='status', header='Status', wrap_class='task-status', attrs={'class': 'centerized'})
    project = Column(field='proj', header='Project')

    class Meta:
        model = Task
        search = True

        attrs = {'class': 'table-striped table-hover'}

class MyAssocTable(Table):

    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='task-detail', 
                args=(
                    A('task.id'),
                ),
                attrs={
                    'class':
                        'glyphicon glyphicon-eye-open'
                },
            ),
        ],
        searchable=False,
        sortable=False,
    )

    brief = Column(field='task.brief', header='Brief')
    role = TagColumn(field='tag_type', header='Role', wrap_class='con-task-assoc')
    deadline = NoneableDatetimeColumn(field='task.deadline', header='Deadline', format='%b %d, %Y')
    status = TagColumn(field='task.status', header='Status', wrap_class='task-status', attrs={'class': 'centerized'})
    project = Column(field='task.proj', header='Project')

    class Meta:
        model = TaskContactAssoc
        search = True

        attrs = {'class': 'table-striped table-hover'}

class ProjectTable(Table):

    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='project-detail', 
                args=(
                    A('id'),
                ),
                attrs={
                    'class':
                        'glyphicon glyphicon-eye-open'
                },
            ),
        ],
        searchable=False,
        sortable=False,
    )

    title = Column(field='title', header='Title')
    notes = Column(field='notes', header='Notes')

    #project = Column(field='task.proj', header='Project')

    class Meta:
        model = Project
        search = True

        attrs = {'class': 'table-striped table-hover'}