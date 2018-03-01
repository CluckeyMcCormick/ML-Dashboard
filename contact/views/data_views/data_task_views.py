
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404

#Django Library Imports
from table import views

#Other file imports
from ...models import ContactTypeTag, Task, TaskContactAssoc

from ...tables import (
	contact_tables as tab_con,
)

from .data_list_views import ContactDataBaseView
from . import PKFeedDataView

class Task_AddDataView(PKFeedDataView, ContactDataBaseView, LoginRequiredMixin):
    """
    When it comes to 
    """
    def get_queryset(self):
        qs = super(Task_AddDataView, self).get_queryset()

        assoc_set = TaskContactAssoc.objects.filter(
            task=self.pk_arg, tag_type__in=['as', 'le', 're', 'na']
        )

        qs = qs.exclude(task_assocs__in=assoc_set) 

        return qs

class Task_AddAssignDataView(Task_AddDataView):

    token = tab_con.SelectVolunteerTable.token

    def get_queryset(self):
        qs = super(Task_AddAssignDataView, self).get_queryset()

        task_inst=get_object_or_404(Task, pk=self.pk_arg)

        if task_inst.proj:
            qs = qs.filter(
                proj_assocs__tag_type__in=['as', 'le', 'cr'], 
                proj_assocs__proj=task_inst.proj
            )
        
        qs = qs.filter(tags__tag_type__in=['vo'])
        return qs

class Task_AddTargetDataView(Task_AddDataView):

    token = tab_con.SelectTargetTable.token

class Task_AddResourceDataView(Task_AddDataView):

    token = tab_con.SelectResourceTable.token
