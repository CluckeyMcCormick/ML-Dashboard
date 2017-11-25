from django.shortcuts import render
from django.views import generic

from .models import Organization, Contact, Project, ContactTypeTag, Task
# Create your views here.

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

def my_dashboard(request):
    """
    View function for the current user's dashboard
    """
    #Get the associated contact for our user
    user_con  = request.user.contact

    #Get the projects associated with the user
    user_proj = user_con.project_set

    #Get the tasks associated with the user
    user_task = user_con.taskcontactassoc_set.exclude(tag_type__exact='ta').exclude(task__complete__exact=True)

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'my_dashboard.html',
        context={
            'user_con':user_con,
            'user_proj':user_proj,
            'user_task':user_task,
        },
    )

def my_dashboard_complete(request):
    """
    View function for the current user's dashboard, showing completed tasks
    """
    #Get the associated contact for our user
    user_con  = request.user.contact

    #Get the projects associated with the user
    user_proj = user_con.project_set

    #Get the tasks associated with the user
    user_task = user_con.taskcontactassoc_set.exclude(tag_type__exact='ta')

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'my_dashboard.html',
        context={
            'user_con':user_con,
            'user_proj':user_proj,
            'user_task':user_task,
        },
    )

# CONTACTS, BRUH! ~~~~~~~~~~~~~~~~~~~~~~
class ContactListView(generic.ListView):
    model = Contact
    context_object_name = 'contact_list' 
    template_name = 'contacts/contact_list.html'

class ContactDetailView(generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'


# PROJECTS, MAH BOI! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ProjectListView(generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


# TASKS, MOUH MAHN! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TaskListView(generic.ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'tasks/task_list.html'

class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
