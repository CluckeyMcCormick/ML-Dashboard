from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render

from django.shortcuts import render, redirect

from django.views import generic

import datetime

from ..forms import UserForm

from ..models import (
    ContactTypeTag, Organization, 
    Contact, Project,
)

from ..tables import (
    assoc_tables   as table_assoc,
    project_tables as table_proj,
    task_tables    as table_task,
    user_tables    as table_user
) 

from .proj_con_assoc_views import get_tiered_proj_assoc_qs
from .task_con_assoc_views import get_tiered_task_assoc_qs

def get_tiered_upcoming(user_con):
    qs_proj_assoc = get_tiered_proj_assoc_qs(user_con)
    qs_proj_assoc = qs_proj_assoc.exclude(proj__complete__exact=True, proj__deadline__lte=datetime.date.today())
    qs_proj_assoc = qs_proj_assoc.exclude(proj__complete__exact=True, proj__deadline__exact=None)

    qs_task_assoc = get_tiered_task_assoc_qs(user_con)
    qs_task_assoc = qs_task_assoc.exclude(task__complete__exact=True, task__deadline__lte=datetime.date.today())
    qs_task_assoc = qs_task_assoc.exclude(task__complete__exact=True, task__deadline__exact=None)

    return qs_proj_assoc, qs_task_assoc

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
    user_con = request.user.contact
    qs_proj_assoc, qs_task_assoc = get_tiered_upcoming(user_con)

    #Get the projects associated with the user
    user_proj_table = table_proj.ProjectAssocAjaxTable(qs_proj_assoc)
    #Get the tasks associated with the user
    user_task_table = table_task.TaskAssocAjaxTable(qs_task_assoc)

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'my_dashboard.html',
        context={
            'user_con':user_con,
            'user_proj_table':user_proj_table,
            'user_task_table':user_task_table,
            'project_source' : 'data-dashboard-project-upcoming',
            'task_source' : 'data-dashboard-task-upcoming',
            'input_id' : user_con.pk,
            'print_url':reverse_lazy('my-dashboard-print'),
        },
    )

@login_required
def my_dashboard_print(request):
    """
    View function for the current user's dashboard
    """
    #Get the associated contact for our user
    user_con = request.user.contact
    qs_proj_assoc, qs_task_assoc = get_tiered_upcoming(user_con)

    #Get the projects associated with the user
    user_proj_table = table_assoc.ProjectAssocTable_Printable(qs_proj_assoc)
    #Get the tasks associated with the user
    user_task_table = table_assoc.TaskAssocTable_Printable(qs_task_assoc)

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'my_dashboard_printable.html',
        context={
            'user_con':user_con,
            'user_proj_table':user_proj_table,
            'user_task_table':user_task_table,
        },
    )

class UserCreateView(PermissionRequiredMixin, generic.edit.FormView):
    template_name = 'users/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('view-users')

    permission_required = 'auth.add_user'

    def form_valid(self, form):
        form.update_user_contact()
        return HttpResponseRedirect( reverse_lazy('view-users') )

class UserListView(UserPassesTestMixin, generic.TemplateView):
    template_name = 'users/user_list.html'

    def test_func(self):
        return self.request.user.has_perm("auth.add_user") \
        or self.request.user.has_perm("auth.change_user")  \
        or self.request.user.has_perm("auth.delete_user")

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        context['user_table'] = table_user.UserTable(User.objects.get_queryset())

        return context