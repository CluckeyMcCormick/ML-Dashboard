
from table import Table
from table.utils import A
from table.columns import LinkColumn, Link

from ..models import TaskContactAssoc, ProjectContactAssoc

from .custom_columns import *
from . import center_attrs, date_time_format

"""
The Assoc models serve as rich relationship join tables.

Since they're meant to just be rich relationship models, we're
generally displaying the information of the two assoc models, with
whatever extra "rich" data we have.

So usually there's two tables per category, one for each end of the
rich relationship.
"""
#___ ____ ____ _  _    ____ ____ _  _    ____ ____ ____ ____ ____ 
# |  |__| [__  |_/  __ |    |  | |\ | __ |__| [__  [__  |  | |    
# |  |  | ___] | \_    |___ |__| | \|    |  | ___] ___] |__| |___ 
#
class TaskAssocTable_Printable(Table):
    """
    Meant to be used from the "perspective" of a single Contact.
    Displays the associated tasks, and the Contact's role in each.
    """
    brief = CustomNoneColumn(field='task.brief', header='Brief')
    role = TagColumn(field='tag_type', header='Role', wrap_class='con-task-assoc')
    deadline = NoneableDatetimeColumn(field='task.deadline', header='Deadline', format=date_time_format)
    status = TagColumn(field='task.status', header='Status', wrap_class='task-status', attrs=center_attrs)
    project = CustomNoneColumn(field='task.proj', header='Project')

    class Meta:
        model = TaskContactAssoc
        search = False
        pagination = False
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class TaskAssocViewMixin(Table):
        
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

class TaskAssocTable(TaskAssocViewMixin, TaskAssocTable_Printable):

    class Meta:
        model = TaskContactAssoc
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

class ContactTaskTable_Basic(Table):
    """
    Meant to be used from the "perspective" of a single Task.
    Displays the associated contacts, and the role of each.
    """

    name = CustomNoneColumn(field='con.name', header='Name')
    role = TagColumn(field='tag_type', header='Role', wrap_class='con-task-assoc')

    class Meta:
        model = TaskContactAssoc
        search = True
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ContactTaskTable_Link(Table):
    """
    Meant to be used from the "perspective" of a single Task.
    Displays the associated contacts, and the role of each.
    """
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='contact-detail', 
                args=(
                    A('con.id'),
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

    class Meta:
        model = TaskContactAssoc
        search = True
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ContactTaskTable(ContactTaskTable_Link, ContactTaskTable_Basic):
    """
    Meant to be used from the "perspective" of a single TASK.
    Displays the associated contacts, and the role of each.
    """
    class Meta:
        model = TaskContactAssoc
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

class ContactTaskTable_Printable(ContactTaskTable_Basic):
    """
    Meant to be used from the "perspective" of a single TASK.
    Displays the associated contacts, and the role of each.
    """

    class Meta:
        model = TaskContactAssoc
        search = False
        pagination = False
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ContactTaskTable_Remove(ContactTaskTable):
    """
    Meant to be used from the "perspective" of a single TASK.
    Displays the associated contacts, and the role of each.
    """
    remove = RemoveConfirmColumn(
        extra_field='con.name', 
        message='''Are you sure you want to remove {0} from this task?''',
        b_name='assoc_id'
    )

    class Meta:
        model = TaskContactAssoc
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

#___  ____ ____  _    ____ ____ _  _    ____ ____ ____ ____ ____ 
#|__] |__/ |  |  | __ |    |  | |\ | __ |__| [__  [__  |  | |    
#|    |  \ |__| _|    |___ |__| | \|    |  | ___] ___] |__| |___ 
#

# This table is "Contact" looking at "Project"
# So we mostly want to display the values of "Project"
class ProjectAssocTable_Printable(Table):
    """
    Meant to be used from the "perspective" of a single Contact.
    Displays the associated projects, and the Contact's role in each.
    """
    title = CustomNoneColumn(field='proj.title', header='Title')
    role = TagColumn(field='tag_type', header='Role', wrap_class='con-task-assoc')
    deadline = NoneableDatetimeColumn(field='proj.deadline', header='Deadline', format=date_time_format)   
    status = TagColumn(field='proj.status', header='Status', wrap_class='task-status', attrs=center_attrs)

    class Meta:
        model = ProjectContactAssoc
        search = False
        pagination = False
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ProjectAssocViewMixin(Table):
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='project-detail', 
                args=(
                    A('proj.id'),
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

class ContactProjectTable_Basic(Table):
    """
    Meant to be used from the "perspective" of a single Project.
    Displays the associated contacts, and the role of each.
    """

    name = CustomNoneColumn(field='con.name', header='Name')
    role = TagColumn(field='tag_type', header='Role', wrap_class='con-task-assoc')

    class Meta:
        model = ProjectContactAssoc
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

class ContactProjectTable_Link(Table):
    """
    Meant to be used from the "perspective" of a single Project.
    Displays the associated contacts, and the role of each.
    """
    view =  LinkColumn(
        header='View', 
        links=[
            Link(
                text='',
                viewname='contact-detail', 
                args=(
                    A('con.id'),
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

    class Meta:
        model = ProjectContactAssoc
        search = True
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ContactProjectTable(ContactProjectTable_Link, ContactProjectTable_Basic):
    """
    Meant to be used from the "perspective" of a single Project.
    Displays the associated contacts, and the role of each.
    """
    class Meta:
        model = ProjectContactAssoc
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}

class ContactProjectTable_Printable(ContactProjectTable_Basic):
    """
    Meant to be used from the "perspective" of a single Project.
    Displays the associated contacts, and the role of each.
    """

    class Meta:
        model = ProjectContactAssoc
        search = False
        pagination = False
        ajax = False

        attrs = {'class': 'table-striped table-hover'}

class ContactProjectTable_Remove(ContactProjectTable):
    """
    Meant to be used from the "perspective" of a single Project.
    Displays the associated contacts, and the role of each.
    """
    remove = RemoveConfirmColumn(
        extra_field='con.name', 
        message='''Are you sure you want to remove {0} from this project? Note that they won\\'t be removed from any assigned tasks! ''',
        b_name='assoc_id'
    )

    class Meta:
        model = ProjectContactAssoc
        search = True
        ajax = False #True

        attrs = {'class': 'table-striped table-hover'}
