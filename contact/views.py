from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic

from .models import ContactTypeTag, Task, TaskContactAssoc
from .models import Organization, Contact, Project

from .forms import MyTaskSearchForm, ContactForm, ProjectForm, TaskForm

from .tables import ContactTable, TaskTable, MyAssocTable, ProjectTable
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

    #Get the projects associated with the user
    user_proj = user_con.associated_projects

    #Get the tasks associated with the user
    user_task = user_con.task_assocs.exclude(tag_type__exact='ta').exclude(task__complete__exact=True)

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

@login_required
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
class ContactListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'contacts/contact_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)

        context['contact_table'] = ContactTable()

        return context

class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)

        context['contact_edit_url'] = reverse_lazy('contact-update', args=(context['contact'].pk,))
        context['contact_delete_url'] = reverse_lazy('contact-delete', args=(context['contact'].pk,))

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


# PROJECTS, MAH BOI! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        context['project_table'] = ProjectTable()
        return context

    
class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        context['project_edit_url'] = reverse_lazy('project-update', args=(context['project'].pk,))
        context['project_delete_url'] = reverse_lazy('project-delete', args=(context['project'].pk,))
        context['new_project_task_url'] = reverse_lazy('task-project-create', args=(context['project'].pk,))
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

# TASKS, MOUH MAHN! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TaskListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['task_table'] = TaskTable()

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

# TASKS CONTACT ASSOCIATIONS, MIJO! ~~~~~~~~~~~~~
class MyTaskView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'con_task_assocs/my_assoc.html'

    def get_context_data(self, **kwargs):
        context = super(MyTaskView, self).get_context_data(**kwargs)
        
        form = MyTaskSearchForm(self.request.GET)

        #Get the tasks associated with the user
        context['form'] = form

        user_con = self.request.user.contact
        context['my_task_table'] = MyAssocTable(user_con.task_assocs.exclude(tag_type__exact='ta'))

        return context
