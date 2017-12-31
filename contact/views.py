from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic

import datetime

from .models import (
    ContactTypeTag, Task, TaskContactAssoc,
    Organization, Contact, Project,
    ProjectContactAssoc,
)

from .forms import ContactForm, ProjectForm, TaskForm, OrgForm
from .tables import (
    assoc_tables        as table_assoc,
    contact_tables      as table_con,
    organization_tables as table_org,
    project_tables      as table_proj,
    task_tables         as table_task
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

    qs_task_assoc = user_con.task_assocs.exclude(tag_type__exact='ta')
    qs_task_assoc = qs_task_assoc.exclude(task__complete__exact=True, task__deadline__lte=datetime.date.today())
    qs_task_assoc = qs_task_assoc.exclude(task__complete__exact=True, task__deadline__exact=None)
    #qs_task_assoc.exclude(task__complete__exact=True, task__deadline__exact=None)

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

#____ ____ _  _ ___ ____ ____ ___    _  _ _ ____ _ _ _ ____ 
#|    |  | |\ |  |  |__| |     |     |  | | |___ | | | [__  
#|___ |__| | \|  |  |  | |___  |      \/  | |___ |_|_| ___] 
#
class ContactListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'contacts/contact_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)

        context['contact_table'] = table_con.ContactTable()

        return context

class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)

        context['contact_edit_url'] = reverse_lazy('contact-update', args=(context['contact'].pk,))
        context['contact_delete_url'] = reverse_lazy('contact-delete', args=(context['contact'].pk,))

        context['associated_projects_table'] = table_assoc.ProjCon_Project_Table( self.object.proj_assocs.get_queryset() )
        context['associated_tasks_table'] = table_assoc.TaskCon_Task_Table( self.object.task_assocs.get_queryset() )

        return context

class ContactCreate(LoginRequiredMixin, CreateView):
    template_name = 'contacts/contact_form.html'
    form_class = ContactForm
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_contact = form.save()
        form.handle_contact_tags(new_contact)
        
        return HttpResponseRedirect(reverse_lazy('contact-detail', args=(new_contact.pk,)))

class ContactUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'contacts/contact_form.html'
    form_class = ContactForm
    model = Contact

    def get_initial(self):
        initial = super(ContactUpdate, self).get_initial()

        initial['con_type'] = []

        tag_coll = ContactTypeTag.objects.filter(contact__exact=self.object.pk)
        
        for tag in tag_coll:
            initial['con_type'].append(tag.tag_type)

        return initial

    def get_context_data(self, **kwargs):
        context = super(ContactUpdate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = False

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        updated_contact = form.save()
        form.handle_contact_tags(updated_contact)
        
        return HttpResponseRedirect(reverse_lazy('contact-detail', args=(updated_contact.pk,)))

class ContactDelete(LoginRequiredMixin, DeleteView):
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts')
    model = Contact

#____ ____ ____ ____ _  _ _ ___  ____ ___ _ ____ _  _    _  _ _ ____ _ _ _ ____ 
#|  | |__/ | __ |__| |\ | |   /  |__|  |  | |  | |\ |    |  | | |___ | | | [__  
#|__| |  \ |__] |  | | \| |  /__ |  |  |  | |__| | \|     \/  | |___ |_|_| ___] 
#
class OrgListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'organizations/org_list.html'

    def get_context_data(self, **kwargs):
        context = super(OrgListView, self).get_context_data(**kwargs)

        context['org_table'] = table_org.OrgTable()

        return context

class OrgDetailView(LoginRequiredMixin, generic.DetailView):
    model = Organization
    template_name = 'organizations/org_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrgDetailView, self).get_context_data(**kwargs)

        context['org_edit_url'] = reverse_lazy('org-update', args=(context['organization'].pk,))
        context['org_delete_url'] = reverse_lazy('org-delete', args=(context['organization'].pk,))
        context['associated_contact_table'] = table_con.ContactTable( Contact.objects.filter(org__exact=self.object) ) 

        return context

class OrgCreate(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'organizations/org_form.html'
    form_class = OrgForm
    success_url = reverse_lazy('org-detail')

    def get_context_data(self, **kwargs):
        context = super(OrgCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

    def form_valid(self, form):
        updated_org = form.save()       
        return HttpResponseRedirect(reverse_lazy('org-detail', args=(updated_org.pk,)))

class OrgUpdate(LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'organizations/org_form.html'
    form_class = OrgForm
    success_url = reverse_lazy('org-detail')

    def form_valid(self, form):
        updated_org = form.save()       
        return HttpResponseRedirect(reverse_lazy('org-detail', args=(updated_org.pk,)))

class OrgDelete(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'organizations/org_confirm_delete.html'
    success_url = reverse_lazy('orgs')

#___  ____ ____  _ ____ ____ ___    _  _ _ ____ _ _ _ ____ 
#|__] |__/ |  |  | |___ |     |     |  | | |___ | | | [__  
#|    |  \ |__| _| |___ |___  |      \/  | |___ |_|_| ___] 
#                                                          
class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        context['project_table'] = table_proj.ProjectTable()
        return context

    
class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        context['project_edit_url'] = reverse_lazy('project-update', args=(context['project'].pk,))
        context['project_delete_url'] = reverse_lazy('project-delete', args=(context['project'].pk,))

        context['project_assign_url'] = reverse_lazy('project-assign')

        context['new_project_task_url'] = reverse_lazy('task-project-create', args=(context['project'].pk,))

        context['associated_contact_table'] = table_assoc.ProjCon_Contact_Table( self.object.con_assocs.get_queryset() )
        context['associated_task_table'] = table_task.TaskNoProjectTable(self.object.tasks.get_queryset())

        return context

class ProjectCreate(LoginRequiredMixin, CreateView):
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_proj = form.save()
        
        creator_assoc = ProjectContactAssoc(con=self.request.user.contact, proj=new_proj, tag_type='cr')
        creator_assoc.save()

        return HttpResponseRedirect(reverse_lazy('project-detail', args=(new_proj.pk,)))


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

class ProjectDelete(LoginRequiredMixin, DeleteView):
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects')
    model = Project

#___ ____ ____ _  _    _  _ _ ____ _ _ _ ____ 
# |  |__| [__  |_/     |  | | |___ | | | [__  
# |  |  | ___] | \_     \/  | |___ |_|_| ___] 
#                                             
class TaskListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['task_table'] = table_task.TaskTable()

        return context

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)

        context['edit_url'] = reverse_lazy('task-update', args=(context['task'].pk,))
        context['delete_url'] = reverse_lazy('task-delete', args=(context['task'].pk,))

        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_task = form.save()
        
        creator_assoc = TaskContactAssoc(con=self.request.user.contact, task=new_task, tag_type='cr')
        creator_assoc.save()
        form.handle_task_assignments(new_task)

        return HttpResponseRedirect(reverse_lazy('task-detail', args=(new_task.pk,)))

class TaskUnboundCreate(TaskCreate):

    def get_form(self):
        form = super(TaskUnboundCreate, self).get_form()

        form.fields['proj'].disabled = True

        return form

class TaskProjectCreate(TaskUnboundCreate):

    def get_initial(self):
        initial = super(TaskUnboundCreate, self).get_initial()
        initial['proj'] = self.kwargs['pk']

        return initial

    def get_context_data(self, **kwargs):
        context = super(TaskProjectCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_bound'] = True

        return context

class TaskUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    model = Task

    def get_initial(self):
        initial = super(TaskUpdate, self).get_initial()

        id_query = TaskContactAssoc.objects.filter(task__exact=self.object.pk, tag_type__in=['as','ta'])

        assigned_query = Contact.objects.filter(task_assocs__in=id_query.filter(tag_type__exact='as'))
        target_query = Contact.objects.filter(task_assocs__in=id_query.filter(tag_type__exact='ta'))

        initial['volunteers'] = []
        initial['targets'] = []

        for vol_val in assigned_query.values_list('id', flat=True):
            initial['volunteers'].append(vol_val)

        for tar_val in target_query.values_list('id', flat=True):
            initial['targets'].append(tar_val)

        return initial

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = False

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_task = form.save()
        
        form.handle_task_assignments(new_task)

        return HttpResponseRedirect(reverse_lazy('task-detail', args=(new_task.pk,)))

class TaskDelete(LoginRequiredMixin, DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    model = Task

#___ ____ ____ _  _    ____ ____ _  _    ____ ____ ____ ____ ____ 
# |  |__| [__  |_/  __ |    |  | |\ | __ |__| [__  [__  |  | |    
# |  |  | ___] | \_    |___ |__| | \|    |  | ___] ___] |__| |___ 
#                                                                 
#_  _ _ ____ _ _ _ ____ 
#|  | | |___ | | | [__  
# \/  | |___ |_|_| ___] 
#                       
class MyTaskView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'con_task_assocs/my_assoc.html'

    def get_context_data(self, **kwargs):
        context = super(MyTaskView, self).get_context_data(**kwargs)

        user_con = self.request.user.contact
        context['my_task_table'] = table_assoc.TaskCon_Task_Table(user_con.task_assocs.exclude(tag_type__exact='ta'))

        return context

#___  ____ ____  _    ____ ____ _  _    ____ ____ ____ ____ ____ 
#|__] |__/ |  |  | __ |    |  | |\ | __ |__| [__  [__  |  | |    
#|    |  \ |__| _|    |___ |__| | \|    |  | ___] ___] |__| |___ 
#                                                                
#_  _ _ ____ _ _ _ ____ 
#|  | | |___ | | | [__  
# \/  | |___ |_|_| ___] 
#                       
class AssignContactView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'proj_con_assocs/assign_form.html'

    def get_context_data(self, **kwargs):
        context = super(AssignContactView, self).get_context_data(**kwargs)

        user_con = self.request.user.contact
        context['assign_table'] = table_con.SelectContactTable(Contact.objects.get_queryset())

        return context

