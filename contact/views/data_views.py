from django.db.models import (
    Case, CharField, Count, ExpressionWrapper,
    Exists, F, FloatField, IntegerField, 
    OuterRef, Q, Subquery, When, Value
)
from django.db.models.functions import Concat

from table import views

from ..models import ContactTypeTag, Task, ProjectContactAssoc

from ..tables import (
	contact_tables      as tab_con,
    organization_tables as tab_org,
    event_tables        as tab_eve,
    project_tables      as tab_proj,
    task_tables         as tab_task
)

import datetime
import math

class ContactDataView(views.FeedDataView):

    token = tab_con.ContactTable.token

    def get_queryset(self):
        q_set = super(ContactDataView, self).get_queryset()

        type_tag_qset = ContactTypeTag.objects.get_queryset()
        type_tag_qset = type_tag_qset.filter(contact=OuterRef('pk'))
        """
        TO APPEND:
            is_volunteer, is_prospect, is_donor
            is_resource, is_foundation
        """
        volu_tag_set = type_tag_qset.filter(tag_type='vo')
        pros_tag_set = type_tag_qset.filter(tag_type='pr')
        dono_tag_set = type_tag_qset.filter(tag_type='do')
        reso_tag_set = type_tag_qset.filter(tag_type='_f')
        foun_tag_set = type_tag_qset.filter(tag_type='_g')

        q_set = q_set.annotate( volu_mark = Exists(volu_tag_set) )
        q_set = q_set.annotate( pros_mark = Exists(pros_tag_set) )
        q_set = q_set.annotate( dono_mark = Exists(dono_tag_set) )
        q_set = q_set.annotate( reso_mark = Exists(reso_tag_set) )
        q_set = q_set.annotate( foun_mark = Exists(foun_tag_set) )

        #print("VOLU")
        q_set = q_set.annotate( 
            ajax_volunteer = Case(
                When( volu_mark=True, then=Value('Volunteer')),
                default=Value(''),
                output_field=CharField() 
            )
        )

        #print("PROS")
        q_set = q_set.annotate( 
            ajax_prospect = Case(
                When( pros_mark=True, then=Value('Prospect')),
                default=Value(''),
                output_field=CharField() 
            ) 
        )

        #print("DONO")
        q_set = q_set.annotate( 
            ajax_donor = Case(
                When( dono_mark=True, then=Value('Donor')),
                default=Value(''),
                output_field=CharField() 
            ) 
        )

        #print("RESO")
        q_set = q_set.annotate( 
            ajax_resource = Case(
                When( reso_mark=True, then=Value('Resource')),
                default=Value(''),
                output_field=CharField() 
            ) 
        )

        #print("FOUN")
        q_set = q_set.annotate( 
            ajax_foundation = Case(
                When( foun_mark=True, then=Value('Foundation Corporation')),
                default=Value(''),
                output_field=CharField() 
            ) 
        )

        return q_set

class OrganizationDataView(views.FeedDataView):

    token = tab_org.OrgTable.token

    def get_queryset(self):
        q_set = super(OrganizationDataView, self).get_queryset()
        return q_set.annotate( num_contacts=Count('contacts') )

class EventDataView(views.FeedDataView):

    token = tab_eve.EventTable.token

    def get_queryset(self):
        q_set = super(EventDataView, self).get_queryset()
        return q_set.annotate( num_contacts=Count('contacts') )

class ProjectDataView(views.FeedDataView):

    token = tab_proj.ProjectTable.token

    def get_queryset(self):
        q_set = super(ProjectDataView, self).get_queryset()

        q_set = q_set.annotate( num_tasks=Count('tasks') )
        q_set = q_set.annotate( num_tasks_complete=Count('tasks', filter=Q(tasks__complete=True)) )

        q_set = q_set.annotate(
            ajax_completion= Concat(
                'num_tasks_complete', Value(" / "), 'num_tasks',
                output_field=CharField()
            )
        )

        q_set = q_set.annotate( 
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

        return q_set

class TaskDataView(views.FeedDataView):

    token = tab_task.TaskTable.token

    def get_queryset(self):
        q_set = super(TaskDataView, self).get_queryset()
        q_set = q_set.annotate( 
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

        return q_set

class PKFeedDataView(views.FeedDataView):
    """
    Some of our data feeds require a pk argument.
    But the get_queryset method won't give it to them!
    That's just fine - we'll use this to save the primary 
    key so we can use it later.
    """
    def get(self, request, *args, **kwargs):
        self.pk_arg = kwargs['pk']
        return super(PKFeedDataView, self).get(request, *args, **kwargs)

class AddLeadDataView(PKFeedDataView, ContactDataView):

    token = tab_con.SelectLeadTable.token

    def get_queryset(self):
        qs = super(AddLeadDataView, self).get_queryset()

        project_id = self.pk_arg
        print("PROJECT ID {0}")
        print(project_id)
        print()

        print(self.token)
        for key, value in self.request.GET.items():
            print("{0} : {1}".format(key, value))

        if project_id:
            assoc_set = ProjectContactAssoc.objects.filter(
                proj=project_id, tag_type__in=['as', 'le', 're', 'na']
            )
            qs = qs.exclude(proj_assocs__in=assoc_set) 

        qs = qs.filter(tags__tag_type__in=['vo'])

        return qs

