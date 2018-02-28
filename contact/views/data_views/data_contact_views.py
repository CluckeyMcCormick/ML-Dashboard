
from django.db.models import (
    Case, CharField, Count, Exists, 
    F, OuterRef, Q, When, Value
)

from django.shortcuts import get_object_or_404

#Django Library Imports
from table import views

import datetime

#Other file imports
from ...models import Contact

from ...tables import (
    assoc_tables as tab_assoc,
    event_tables as tab_event,
    project_tables as tab_proj,
    task_tables as tab_task
)

from ..proj_con_assoc_views import get_tiered_proj_assoc_qs
from ..task_con_assoc_views import get_tiered_task_assoc_qs

from . import PKFeedDataView

class Contact_TaskDataView(PKFeedDataView):

    token = tab_task.TaskAssocAjaxTable.token

    def get_queryset(self):
        qs = super(Contact_TaskDataView, self).get_queryset()

        assoc_set = get_object_or_404(Contact, pk=self.pk_arg).task_assocs.get_queryset()

        qs = qs.filter(contacts__pk=self.pk_arg).distinct()

        #limit the assocs
        assigned_set = assoc_set.filter(task=OuterRef('pk'), tag_type='as')
        resource_set = assoc_set.filter(task=OuterRef('pk'), tag_type='re')
        target_set = assoc_set.filter(task=OuterRef('pk'), tag_type='ta')
        creator_set = assoc_set.filter(task=OuterRef('pk'), tag_type='cr')

        #Annotate whether the assoc exists for each task
        qs = qs.annotate( assigned_mark = Exists(assigned_set) )
        qs = qs.annotate( resource_mark = Exists(resource_set) )
        qs = qs.annotate( target_mark = Exists(target_set) )
        qs = qs.annotate( creator_mark = Exists(creator_set) )

        qs = qs.annotate( 
            ajax_tag_type = Case(
                # when assigned tag exists, 'Assigned'
                When( assigned_mark=True, then=Value('Assigned') ),
                # when resource tag exists, 'Resource'
                When( resource_mark=True, then=Value('Resource') ),
                # when target tag exists, 'Target'
                When( target_mark=True, then=Value('Target') ),
                # when target tag exists, 'Creator'
                When( creator_mark=True, then=Value('Creator') ),
                default=Value('Unspecified'),
                output_field=CharField() 
            ) 
        )

        qs = qs.annotate( 
            ajax_status = Case(
                When( complete=True, then=Value('Completed') ),
                When( 
                    Q( deadline=None ) | Q( deadline__gt=datetime.date.today() ), 
                    then=Value('Incomplete')
                ),
                default=Value('Overdue'),
                output_field=CharField() 
            ) 
        )

        return qs

class Contact_ProjectDataView(PKFeedDataView):

    token = tab_proj.ProjectAssocAjaxTable.token

    def get_queryset(self):
        qs = super(Contact_ProjectDataView, self).get_queryset()

        assoc_set = get_object_or_404(Contact, pk=self.pk_arg).proj_assocs.get_queryset()

        qs = qs.filter(contacts__pk=self.pk_arg).distinct()

        #limit the assocs
        lead_set = assoc_set.filter(proj=OuterRef('pk'), tag_type='le')
        assigned_set = assoc_set.filter(proj=OuterRef('pk'), tag_type='as')
        resource_set = assoc_set.filter(proj=OuterRef('pk'), tag_type='re')
        creator_set = assoc_set.filter(proj=OuterRef('pk'), tag_type='cr')

        #Annotate whether the assoc exists for each proj
        qs = qs.annotate( lead_mark = Exists(lead_set) )
        qs = qs.annotate( assigned_mark = Exists(assigned_set) )
        qs = qs.annotate( resource_mark = Exists(resource_set) )
        qs = qs.annotate( creator_mark = Exists(creator_set) )

        qs = qs.annotate( 
            ajax_tag_type = Case(
                # when lead tag exists, 'Lead'
                When( lead_mark=True, then=Value('Project Lead') ),
                # when assigned tag exists, 'Assigned'
                When( assigned_mark=True, then=Value('Assigned') ),
                # when resource tag exists, 'Resource'
                When( resource_mark=True, then=Value('Resource') ),
                # when target tag exists, 'Creator'
                When( creator_mark=True, then=Value('Creator') ),
                default=Value('Unspecified'),
                output_field=CharField() 
            ) 
        )

        qs = qs.annotate( 
            ajax_status = Case(
                When( complete=True, then=Value('Completed') ),
                When( 
                    Q( deadline=None ) | Q( deadline__gt=datetime.date.today() ), 
                    then=Value('Incomplete')
                ),
                default=Value('Overdue'),
                output_field=CharField() 
            ) 
        )

        return qs

class Contact_EventDataView(PKFeedDataView):

    token = tab_event.EventTable_Basic.token

    def get_queryset(self):
        qs = super(Contact_EventDataView, self).get_queryset()
        qs = qs.filter(contacts__pk__in=[self.pk_arg])

        return qs

