from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, CheckboxColumn

from ..models import Event

from .custom_columns import *

#____ ____ ____ ____ _  _ _ ___  ____ ___ _ ____ _  _ 
#|  | |__/ | __ |__| |\ | |   /  |__|  |  | |  | |\ | 
#|__| |  \ |__] |  | | \| |  /__ |  |  |  | |__| | \| 
#
class EventTable(Table):
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='event-detail', 
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

    name = CustomNoneColumn(field='name', header='Name')
    cons = Column(field='contact_count', header='Contacts')
    notes = CustomNoneColumn(field='notes_bleach_trim', header='Notes')

    class Meta:
        model = Event
        search = True

        attrs = {'class': 'table-striped table-hover'}           

class EventTable_Printable(Table):
    name = CustomNoneColumn(field='name', header='Name')
    cons = Column(field='contact_count', header='Contacts')
    notes = CustomNoneColumn(field='notes_bleach_trim', header='Notes')

    class Meta:
        model = Event
        search = False
        pagination = False
        attrs = {'class': 'table-striped table-hover'}           
