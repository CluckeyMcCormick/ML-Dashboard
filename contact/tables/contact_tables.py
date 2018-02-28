from django.urls import reverse_lazy

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
class ContactViewMixin(Table):
    """
    A link to a contact
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

class ContactNameMixin(Table):
    """
    A name column.
    """
    name = CustomNoneColumn(field='name', header='Name')

class ContactOrgMixin(Table):
    """
    An organization column.
    """
    org = CustomNoneColumn(field='org.name', header='Organization')

class ContactBasicMixin(ContactViewMixin, ContactNameMixin, ContactOrgMixin):
    """
    Concatenates the basic columns - view, name, and org
    """

class ContactInfoMixin(Table):
    """
    Columns for Contact's contact info - email and phone number.
    """
    email = CustomNoneColumn(field='email', header='E-Mail')
    phone = CustomNoneColumn(field='phone', header='Phone')

class ContactNotesMixin(Table):
    """
    A single column - a clipping of the contact's notes
    """
    notes = BleachTrimColumn(field='notes', header='Notes')      

class ContactTagMixin(Table):
    """
    Columns to display a Contact's Type Tag info.
    """
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

class ContactAjaxTagMixin(Table):
    """
    Columns to display a Contact's Type Tag info.
    """
    is_volunteer = CheckOnlyColumn(
        field='ajax_volunteer', header='Volunteer', 
        true_class='contag icon vo', 
        attrs=center_attrs,)

    is_prospect = CheckOnlyColumn(
        field='ajax_prospect', header='Prospect', 
        true_class='contag icon pr', 
        attrs=center_attrs,)

    is_donor = CheckOnlyColumn(
        field='ajax_donor', header='Donor', 
        true_class='contag icon do', 
        attrs=center_attrs,)

    is_resource = CheckOnlyColumn(
        field='ajax_resource', header='Grant', 
        true_class='contag icon _g', 
        attrs=center_attrs,)

    is_foundation = CheckOnlyColumn(
        field='ajax_foundation', header='Corp / Foundation', 
        true_class='contag icon _f', 
        attrs=center_attrs,)

#____ ____ _  _ ___ ____ ____ ___ 
#|    |  | |\ |  |  |__| |     |  
#|___ |__| | \|  |  |  | |___  |  
#
class ContactTable(ContactBasicMixin, ContactNotesMixin, ContactAjaxTagMixin):

    class Meta:
        model = Contact
        search = True
        ajax = True
        ajax_source = reverse_lazy('data-contact')

        attrs = {'class': 'table-striped table-hover'}

class ContactOrglessTable_Printable(ContactNameMixin, ContactNotesMixin, ContactTagMixin):

    class Meta:
        model = Contact
        search = False
        pagination = False
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ContactOrglessTable(ContactViewMixin, ContactOrglessTable_Printable):

    class Meta:
        model = Contact
        search = True
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

#____ ____ _    ____ ____ ___    ____ ____ _  _ ___ ____ ____ ___ ____ 
#[__  |___ |    |___ |     |     |    |  | |\ |  |  |__| |     |  [__  
#___] |___ |___ |___ |___  |     |___ |__| | \|  |  |  | |___  |  ___] 
# 
class SelectVolunteerTable(ContactBasicMixin, ContactAjaxTagMixin):
    
    check = AddButtonColumn(b_class='as hoverable', b_name='vol_id')

    class Meta:
        model = Contact
        search = True
        ajax = True
        ajax_source = reverse_lazy('data-contact')

        attrs = {'class': 'table-striped table-hover'}

class SelectTargetTable(ContactBasicMixin, ContactAjaxTagMixin):
    
    check = AddButtonColumn(b_class='ta hoverable', b_name='targ_id')

    class Meta:
        model = Contact
        search = True
        ajax = True
        ajax_source = reverse_lazy('data-contact')

        attrs = {'class': 'table-striped table-hover'}

class SelectResourceTable(ContactBasicMixin, ContactAjaxTagMixin):
    
    check = AddButtonColumn(b_class='re hoverable', b_name='res_id')

    class Meta:
        model = Contact
        search = True
        ajax = True
        ajax_source = reverse_lazy('data-contact')

        attrs = {'class': 'table-striped table-hover'}

class SelectLeadTable(ContactBasicMixin, ContactAjaxTagMixin):
    
    check = AddButtonColumn(b_class='le hoverable', b_name='lead_id')

    class Meta:
        model = Contact
        search = True
        ajax = True
        ajax_source = reverse_lazy('data-contact')

        attrs = {'class': 'table-striped table-hover'}

