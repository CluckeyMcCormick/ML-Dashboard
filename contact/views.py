from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic

from .models import ContactTypeTag, Task, TaskContactAssoc
from .models import Organization, Contact, Project

from .forms import MyTaskSearchForm, ContactForm
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
class ContactListView(LoginRequiredMixin, generic.ListView):
    model = Contact
    context_object_name = 'contact_list' 
    template_name = 'contacts/contact_list.html'

class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)

        context['contact_edit_url'] = reverse_lazy('contact-update', args=(context['contact'].pk,))
        context['contact_delete_url'] = reverse_lazy('contact-delete', args=(context['contact'].pk,))

        return context

class ContactCreate(CreateView):
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

class ContactUpdate(UpdateView):
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

class ContactDelete(DeleteView):
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts')
    model = Contact

# PROJECTS, MAH BOI! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'

class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


# TASKS, MOUH MAHN! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'tasks/task_list.html'

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

# TASKS CONTACT ASSOCIATIONS, MIJO! ~~~~~~~~~~~~~
class MyTaskView(LoginRequiredMixin, generic.ListView):
    model = TaskContactAssoc
    context_object_name = 'assoc_list'
    template_name = 'con_task_assocs/my_assoc.html'
    
    def get_queryset(self):
        user_con = self.request.user.contact
        return user_con.taskcontactassoc_set.exclude(tag_type__exact='ta')

    def get_context_data(self, **kwargs):
        context = super(MyTaskView, self).get_context_data(**kwargs)
        
        form = MyTaskSearchForm(self.request.GET)

        #Get the tasks associated with the user
        context['form'] = form

        return context
