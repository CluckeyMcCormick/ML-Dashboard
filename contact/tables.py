from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, CheckboxColumn

from .custom_columns import *

from .models import (
    ContactTypeTag, Task, TaskContactAssoc,
    Organization, Contact, Project,
)
        
gen_attrs = {'class': 'centerized'}

#____ ____ _  _ ___ ____ ____ ___ 
#|    |  | |\ |  |  |__| |     |  
#|___ |__| | \|  |  |  | |___  |  
#
class ContactTable(Table):
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
    email = CustomNoneColumn(field='email', header='E-Mail')
    phone = CustomNoneColumn(field='phone', header='Phone')
    org = CustomNoneColumn(field='org.name', header='Organization')
    tags = CustomNoneColumn(field='type_list_string', visible=False)

    is_volunteer = CheckOnlyColumn(
        field='is_volunteer', header='Volunteer', 
        true_class='contag icon vo', 
        attrs=gen_attrs,)

    is_prospect = CheckOnlyColumn(
        field='is_prospect', header='Prospect', 
        true_class='contag icon pr', 
        attrs=gen_attrs,)

    is_donor = CheckOnlyColumn(
        field='is_donor', header='Donor', 
        true_class='contag icon do', 
        attrs=gen_attrs,)

    is_resource = CheckOnlyColumn(
        field='is_resource', header='Grant Resource', 
        true_class='contag icon _g', 
        attrs=gen_attrs,)

    is_foundation = CheckOnlyColumn(
        field='is_foundation', header='Corporation / Foundation', 
        true_class='contag icon _f', 
        attrs=gen_attrs,)

    class Meta:
        model = Contact
        search = True

        attrs = {'class': 'table-striped table-hover'}

#____ ____ _    ____ ____ ___    ____ ____ _  _ ___ ____ ____ ___ ____ 
#[__  |___ |    |___ |     |     |    |  | |\ |  |  |__| |     |  [__  
#___] |___ |___ |___ |___  |     |___ |__| | \|  |  |  | |___  |  ___] 
# 
class SelectContactTable(Table):
    check = CheckboxColumn(header='Select')
    name = CustomNoneColumn(field='name', header='Name')
    org = CustomNoneColumn(field='org.name', header='Organization')
    tags = CustomNoneColumn(field='type_list_string', visible=False)

    is_volunteer = CheckOnlyColumn(
        field='is_volunteer', header='Volunteer', 
        true_class='contag icon vo', 
        attrs=gen_attrs,)

    is_prospect = CheckOnlyColumn(
        field='is_prospect', header='Prospect', 
        true_class='contag icon pr', 
        attrs=gen_attrs,)

    is_donor = CheckOnlyColumn(
        field='is_donor', header='Donor', 
        true_class='contag icon do', 
        attrs=gen_attrs,)

    is_resource = CheckOnlyColumn(
        field='is_resource', header='Grant Resource', 
        true_class='contag icon _g', 
        attrs=gen_attrs,)

    is_foundation = CheckOnlyColumn(
        field='is_foundation', header='Corporation / Foundation', 
        true_class='contag icon _f', 
        attrs=gen_attrs,)

    class Meta:
        model = Contact
        search = True

        attrs = {'class': 'table-striped table-hover'}

#___ ____ ____ _  _ 
# |  |__| [__  |_/  
# |  |  | ___] | \_ 
#                   
class TaskTable(Table):
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
    deadline = NoneableDatetimeColumn(field='deadline', header='Deadline', format='%b %d, %Y')
    status = TagColumn(field='status', header='Status', wrap_class='task-status', attrs={'class': 'centerized'})
    project = CustomNoneColumn(field='proj', header='Project')

    class Meta:
        model = Task
        search = True

        attrs = {'class': 'table-striped table-hover'}

#___ ____ ____ _  _    ____ ____ _  _    ____ ____ ____ ____ ____ 
# |  |__| [__  |_/  __ |    |  | |\ | __ |__| [__  [__  |  | |    
# |  |  | ___] | \_    |___ |__| | \|    |  | ___] ___] |__| |___ 
#                                                                            
class TaskConAssocTable(Table):

    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='task-detail', 
                args=(
                    A('task.id'),
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

    brief = CustomNoneColumn(field='task.brief', header='Brief')
    role = TagColumn(field='tag_type', header='Role', wrap_class='con-task-assoc')
    deadline = NoneableDatetimeColumn(field='task.deadline', header='Deadline', format='%b %d, %Y')
    status = TagColumn(field='task.status', header='Status', wrap_class='task-status', attrs={'class': 'centerized'})
    project = CustomNoneColumn(field='task.proj', header='Project')

    class Meta:
        model = TaskContactAssoc
        search = True

        attrs = {'class': 'table-striped table-hover'}

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
    notes = CustomNoneColumn(field='notes', header='Notes')

    class Meta:
        model = Project
        search = True

        attrs = {'class': 'table-striped table-hover'}

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
    cons = Column(field='contacts.count', header='Contacts')
    notes = CustomNoneColumn(field='notes', header='Notes')

    class Meta:
        model = Organization
        search = True

        attrs = {'class': 'table-striped table-hover'}                                                                     


