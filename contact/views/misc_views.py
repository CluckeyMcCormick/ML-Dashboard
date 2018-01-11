from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render

import datetime

from ..models import (
    ContactTypeTag, Organization, 
    Contact, Project,
)

from ..tables import (
    assoc_tables        as table_assoc
) 

# Create your views here.
@login_required
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_orgs=Organization.objects.count()
    num_contacts=Contact.objects.count()
    # Get the number of Volunteers
    num_volunteers=ContactTypeTag.objects.filter(tag_type__exact='vo').count()
    num_projects=Project.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={
            'num_orgs':num_orgs,
            'num_contacts':num_contacts,
            'num_volunteers':num_volunteers,
            'num_projects':num_projects,
        },
    )

@login_required
def my_dashboard(request):
    """
    View function for the current user's dashboard
    """
    #Get the associated contact for our user
    user_con  = request.user.contact

    qs_proj_assoc = user_con.proj_assocs.exclude(tag_type__exact='re')
    qs_proj_assoc = qs_proj_assoc.exclude(proj__complete__exact=True, proj__deadline__lte=datetime.date.today())
    qs_proj_assoc = qs_proj_assoc.exclude(proj__complete__exact=True, proj__deadline__exact=None)

    qs_task_assoc = user_con.task_assocs.exclude(tag_type__in=['ta', 're'])
    qs_task_assoc = qs_task_assoc.exclude(task__complete__exact=True, task__deadline__lte=datetime.date.today())
    qs_task_assoc = qs_task_assoc.exclude(task__complete__exact=True, task__deadline__exact=None)

    #Get the projects associated with the user
    user_proj_table = table_assoc.ProjCon_Project_Table(qs_proj_assoc)
    #Get the tasks associated with the user
    user_task_table = table_assoc.TaskCon_Task_Table(qs_task_assoc)

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'my_dashboard.html',
        context={
            'user_con':user_con,
            'user_proj_table':user_proj_table,
            'user_task_table':user_task_table,
        },
    )
