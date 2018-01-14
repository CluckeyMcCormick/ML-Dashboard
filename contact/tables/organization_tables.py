from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, CheckboxColumn

from ..models import Organization

from .custom_columns import *

#____ ____ ____ ____ _  _ _ ___  ____ ___ _ ____ _  _ 
#|  | |__/ | __ |__| |\ | |   /  |__|  |  | |  | |\ | 
#|__| |  \ |__] |  | | \| |  /__ |  |  |  | |__| | \| 
#
class OrgTable(Table):
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='org-detail', 
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
        model = Organization
        search = True

        attrs = {'class': 'table-striped table-hover'}           
