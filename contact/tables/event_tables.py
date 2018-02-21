
from django.urls import reverse_lazy

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

def get_contact_counts(obj, **kwargs):
    return obj.contacts.count()

class EventGeneralMixin(Table):
    name = CustomNoneColumn(field='name', header='Name')
    cons = CustomNoneColumn(field='num_contacts', header='Contacts')
    notes = BleachTrimColumn(field='notes', header='Notes')

class EventBasicMixin(Table):
    name = CustomNoneColumn(field='name', header='Name')
    notes = BleachTrimColumn(field='notes', header='Notes')

class EventTable(EventLinkMixin, EventGeneralMixin):

    class Meta:
        model = Event
        search = True
        ajax = True
        ajax_source = reverse_lazy('table-data-event')

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
