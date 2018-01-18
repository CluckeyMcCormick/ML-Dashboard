
from table import Table
from table.columns import Column

from ..models import TaskContactAssoc, ProjectContactAssoc

from .custom_columns import FunctionColumn

def get_project_relate_tag(obj, **kwargs):
    contact = obj
    in_project = kwargs['in_project']

    any_but_create = ProjectContactAssoc.objects.filter(
        con=contact, proj=in_project, tag_type__in=['as', 'le', 're', 'na']
    )

    only_create = ProjectContactAssoc.objects.filter(
        con=contact, proj=in_project, tag_type='cr'
    )

    tag = '''<strong class="con-task-assoc {0}">{1}</strong>'''

    if any_but_create.exists():
        assoc = any_but_create.first()
        return tag.format(assoc.tag_type, assoc.get_tag_type_display())
    elif only_create.exists():
        assoc = only_create.first()
        return tag.format(assoc.tag_type, assoc.get_tag_type_display())

    return ''

def get_assignment_tag(obj, **kwargs):
    contact = obj
    in_task = kwargs['in_task']

    any_but_create = TaskContactAssoc.objects.filter(
        con=contact, task=in_task, tag_type__in=['as', 'ta', 're', 'na']
    )

    only_create = TaskContactAssoc.objects.filter(
        con=contact, task=in_task, tag_type='cr'
    )

    tag = '''<strong class="con-task-assoc {0}">{1}</strong>'''

    if any_but_create.exists():
        assoc = any_but_create.first()
        return tag.format(assoc.tag_type, assoc.get_tag_type_display())
    elif only_create.exists():
        assoc = only_create.first()
        return tag.format(assoc.tag_type, assoc.get_tag_type_display())

    return ''

class ProjectContactIntersection(Table):

    name = Column(field='name', header='Name')

    class Meta:
        search = True
        attrs = {'class': 'table-striped table-hover'} 

    def __init__(self, in_query=None, project=None, **kwargs):
        super(ProjectContactIntersection, self).__init__(**kwargs)

        project_assign_col = FunctionColumn(
            header='Project Role',
            extra_kwargs={'in_project' : project},
            function=get_project_relate_tag,
            header_attrs={'width': "115px"}
        )

        self.columns.append(project_assign_col)

        for task in in_query.all():
            new_col = FunctionColumn(
                header='Task: ' + task.brief,
                extra_kwargs={'in_task' : task},
                function=get_assignment_tag,
            )
            self.columns.append(new_col)
