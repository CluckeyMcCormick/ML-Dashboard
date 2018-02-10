from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, CheckboxColumn

from ..models import Project

from .custom_columns import *

from . import date_time_format, center_attrs

#___  ____ ____  _ ____ ____ ___ 
#|__] |__/ |  |  | |___ |     |  
#|    |  \ |__| _| |___ |___  |  
#
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

    title = CustomNoneColumn(field='title', header='Title')
    status = TagColumn(field='status', header='Status', wrap_class='task-status', attrs=center_attrs)
    percent = Column(field='percentage_formatted', header='Completion')
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format=date_time_format)
    notes = Column(field='notes_bleach_trim', header='Notes')

    class Meta:
        model = Project
        search = True
        ajax = True

        attrs = {'class': 'table-striped table-hover'}

