from table import Table
from table.utils import A
from table.columns import LinkColumn, Link, CheckboxColumn

from .custom_columns import *

from ..models import Contact
from . import center_attrs

#_  _ _ _  _ _ _  _ ____ 
#|\/| |  \/  | |\ | [__  
#|  | | _/\_ | | \| ___] 
#
"""
When a table inherits from another table, it inherits the columns as well.
So these mixins specify some basic column groups that we'll re-use.

We can then construct a table by inheriting from these mixins, allowing us
to create consistent tables without repeated code.
"""
class ContactBasicMixin(Table):
    """
    Very basic contact columns - a view, a name, and their organization.
    """
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

    name = CustomNoneColumn(field='name', header='Name')
    org = CustomNoneColumn(field='org.name', header='Organization')

class ContactInfoMixin(Table):
    """
    Columns for Contact's contact info - email and phone number.
    """
    email = CustomNoneColumn(field='email', header='E-Mail')
    phone = CustomNoneColumn(field='phone', header='Phone')

class ContactTagMixin(Table):
    """
    Columns to display a Contact's Type Tag info.
    """
    tags = CustomNoneColumn(field='type_list_string', visible=False)

    is_volunteer = CheckOnlyColumn(
        field='is_volunteer', header='Volunteer', 
        true_class='contag icon vo', 
        attrs=center_attrs,)

    is_prospect = CheckOnlyColumn(
        field='is_prospect', header='Prospect', 
        true_class='contag icon pr', 
        attrs=center_attrs,)

    is_donor = CheckOnlyColumn(
        field='is_donor', header='Donor', 
        true_class='contag icon do', 
        attrs=center_attrs,)

    is_resource = CheckOnlyColumn(
        field='is_resource', header='Grant', 
        true_class='contag icon _g', 
        attrs=center_attrs,)

    is_foundation = CheckOnlyColumn(
        field='is_foundation', header='Corp / Foundation', 
        true_class='contag icon _f', 
        attrs=center_attrs,)

#____ ____ _  _ ___ ____ ____ ___ 
#|    |  | |\ |  |  |__| |     |  
#|___ |__| | \|  |  |  | |___  |  
#
class ContactTable(ContactBasicMixin, ContactInfoMixin, ContactTagMixin):

    class Meta:
        model = Contact
        search = True

        attrs = {'class': 'table-striped table-hover'}

#____ ____ _    ____ ____ ___    ____ ____ _  _ ___ ____ ____ ___ ____ 
#[__  |___ |    |___ |     |     |    |  | |\ |  |  |__| |     |  [__  
#___] |___ |___ |___ |___  |     |___ |__| | \|  |  |  | |___  |  ___] 
# 
class SelectContactTable(ContactBasicMixin, ContactTagMixin):
    
    lead_check = CheckboxColumn(header='Lead', attrs=center_attrs)
    assigned_check = CheckboxColumn(header='Assigned', attrs=center_attrs)
    resource_check = CheckboxColumn(header='Resource', attrs=center_attrs)

    class Meta:
        model = Contact
        search = True

        attrs = {'class': 'table-striped table-hover'}

