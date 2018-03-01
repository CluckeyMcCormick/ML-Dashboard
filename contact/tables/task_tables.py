
from django.urls import reverse_lazy

from table import Table
from table.utils import A
from table.columns import LinkColumn, Link

from ..models import Task

from .custom_columns import *
from . import center_attrs, date_time_format

#___ ____ ____ _  _ 
# |  |__| [__  |_/  
# |  |  | ___] | \_ 
#
class TaskBasicTable(Table):

    brief = CustomNoneColumn(field='brief', header='Brief')
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format=date_time_format)
    
    class Meta:
        model = Task
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

class TaskLinkMixin(Table):

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

class TaskNoProjectTable(TaskLinkMixin, TaskBasicTable):
    """
    Nothing to see here
    """
    status = TagColumn(field='status', header='Status', wrap_class='task-status', attrs=center_attrs)
    
    class Meta:
        model = Task
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

class TaskTable(TaskLinkMixin, TaskBasicTable):

    status = TagColumn(field='ajax_status', header='Status', wrap_class='task-status', attrs=center_attrs)
    project = CustomNoneColumn(field='proj.title', header='Project')
    notes = BleachTrimColumn(field='notes', header='Notes') 

    class Meta:
        model = Task
        search = True
        ajax = True 
        ajax_source = reverse_lazy('data-task')
        attrs = {'class': 'table-striped table-hover'}

class TaskNoProjectTable_Printable(TaskBasicTable):

    class Meta:
        model = Task
        search = False
        pagination = False
        ajax = False
        attrs = {'class': 'table-striped table-hover'}

class TaskAssocAjaxTable(TaskLinkMixin):
    
    brief = CustomNoneColumn(field='brief', header='Brief')
    role = TagColumn(field='ajax_tag_type', header='Role', wrap_class='con-task-assoc')
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format=date_time_format)
    status = TagColumn(field='ajax_status', header='Status', wrap_class='task-status', attrs=center_attrs)
    project = CustomNoneColumn(field='proj', header='Project')

    class Meta:
        model = Task
        search = True
        ajax = True 

        attrs = {'class': 'table-striped table-hover'}

