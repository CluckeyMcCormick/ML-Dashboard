from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, CheckboxColumn

from ..models import Project

from .custom_columns import *

from . import date_time_format

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
    percent = Column(field='percentage_formatted', header='Completion')
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format=date_time_format)
    notes = CustomNoneColumn(field='notes_trimmed', header='Notes')

    class Meta:
        model = Project
        search = True

        attrs = {'class': 'table-striped table-hover'}

