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
class TaskNoProjectTable(Table):
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

    brief = CustomNoneColumn(field='brief', header='Brief')
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format=date_time_format)
    status = TagColumn(field='status', header='Status', wrap_class='task-status', attrs=center_attrs)
    
    class Meta:
        model = Task
        search = True

        attrs = {'class': 'table-striped table-hover'}

class TaskTable(TaskNoProjectTable):

    project = CustomNoneColumn(field='proj', header='Project')

    class Meta:
        model = Task
        search = True

        attrs = {'class': 'table-striped table-hover'}
