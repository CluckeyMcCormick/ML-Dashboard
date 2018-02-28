
#Django Library Imports
from table import views

#Other file imports
from ...models import ContactTypeTag, Task, ProjectContactAssoc

from ...tables import (
	contact_tables      as tab_con,
)

from .data_list_views import ContactDataView
from . import PKFeedDataView

class Project_AddDataView(PKFeedDataView, ContactDataView):
    """
    When it comes to 
    """
    def get_queryset(self):
        qs = super(Project_AddDataView, self).get_queryset()

        assoc_set = ProjectContactAssoc.objects.filter(
            proj=self.pk_arg, tag_type__in=['as', 'le', 're', 'na']
        )

        qs = qs.exclude(proj_assocs__in=assoc_set) 

        return qs


class Project_AddLeadDataView(Project_AddDataView):

    token = tab_con.SelectLeadTable.token

    def get_queryset(self):
        print("GETTING LEAD QUERYSET!")
        qs = super(Project_AddLeadDataView, self).get_queryset()
        qs = qs.filter(tags__tag_type__in=['vo'])
        return qs

class Project_AddAssignDataView(Project_AddDataView):

    token = tab_con.SelectVolunteerTable.token

    def get_queryset(self):
        qs = super(Project_AddAssignDataView, self).get_queryset()
        qs = qs.filter(tags__tag_type__in=['vo'])
        return qs

class Project_AddResourceDataView(Project_AddDataView):

    token = tab_con.SelectResourceTable.token
