from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, CheckboxColumn

from ..models import Event

from .custom_columns import *

#____ _  _ ____ _  _ ___ ____ 
#|___ |  | |___ |\ |  |  [__  
#|___  \/  |___ | \|  |  ___] 
#                             
class EventLinkMixin(Table):
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

def get_contact_count(obj, **kwargs):
    return obj.contact_count

class EventGeneralMixin(Table):
    name = CustomNoneColumn(field='name', header='Name')
    cons = FunctionColumn(field='name', header='Contacts', function=get_contact_count)
    notes = BleachTrimColumn(field='notes', header='Notes')

class EventBasicMixin(Table):
    name = CustomNoneColumn(field='name', header='Name')
    notes = BleachTrimColumn(field='notes', header='Notes')

class EventTable(EventLinkMixin, EventGeneralMixin):

    class Meta:
        model = Event
        search = True
        ajax = True

        attrs = {'class': 'table-striped table-hover'}           

class EventTable_Basic(EventLinkMixin, EventBasicMixin):

    class Meta:
        model = Event
        search = True
        ajax = True

        attrs = {'class': 'table-striped table-hover'}     
        

class EventTable_Printable(EventBasicMixin):

    class Meta:
        model = Event
        search = False
        pagination = False
        ajax = False
        attrs = {'class': 'table-striped table-hover'}           
