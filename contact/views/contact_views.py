from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

import datetime

from ..reports import get_contact_dataset

from ..models import ContactTypeTag, Contact, Task, Project

from ..forms import ContactForm

from ..tables import (
    assoc_tables   as table_assoc,
    contact_tables as table_con,
    event_tables   as table_event,
    project_tables as table_project,
    task_tables as table_task
) 

from .proj_con_assoc_views import get_tiered_proj_assoc_qs
from .task_con_assoc_views import get_tiered_task_assoc_qs

def is_related_contact(con_a, con_b):
    #find all the Contacts where a and b are associated through a common task
    t_que_a = Task.objects.filter(contacts__in=[con_a], con_assocs__tag_type__in=['cr', 'as']).order_by()
    t_que_b = Task.objects.filter(contacts__in=[con_b]).order_by()

    #find all the Contacts where a and b are associated through a common project
    p_que_a = Project.objects.filter(contacts__in=[con_a], con_assocs__tag_type__in=['cr', 'as', 'le']).order_by()
    p_que_b = Project.objects.filter(contacts__in=[con_b]).order_by()

    #find all the Contacts where a is project associated and b is task associated
    p_t_que_a = Project.objects.filter(contacts__in=[con_a], con_assocs__tag_type__in=['cr', 'as', 'le'] ).order_by()
    p_t_que_b = Project.objects.filter(tasks__contacts__in=[con_b]).order_by()

    return t_que_a.intersection(t_que_b).exists() \
    or p_que_a.intersection(p_que_b).exists()     \
    or p_t_que_a.intersection(p_t_que_b).exists() 

#____ ____ _  _ ___ ____ ____ ___    _  _ _ ____ _ _ _ ____ 
#|    |  | |\ |  |  |__| |     |     |  | | |___ | | | [__  
#|___ |__| | \|  |  |  | |___  |      \/  | |___ |_|_| ___] 
#
class ContactListView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'contacts/contact_list.html'
    permission_required = 'contact.contact_view_all'

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)

        context['contact_table'] = table_con.ContactTable()

        context['download_all_url'] = reverse_lazy('contacts-all-download')
        context['download_volunteer_url'] = reverse_lazy('contacts-volunteer-download')
        context['download_prospect_url'] = reverse_lazy('contacts-prospect-download')
        context['download_donor_url'] = reverse_lazy('contacts-donor-download')
        context['download_grant_url'] = reverse_lazy('contacts-grant-download')
        context['download_corporation_url'] = reverse_lazy('contacts-corporation-download')

        return context

class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'

    def test_func(self):
        if self.request.user.has_perm("contact.contact_view_all"):
            return True
        elif self.request.user.has_perm("contact.contact_view_related"):
            this = Contact.objects.get(pk=self.kwargs['pk'])
            return is_related_contact(self.request.user.contact, this)
        return False

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)

        context['contact_print_url'] = reverse_lazy('contact-print', args=(context['contact'].pk,))
        context['contact_edit_url'] = reverse_lazy('contact-update', args=(context['contact'].pk,))
        context['contact_delete_url'] = reverse_lazy('contact-delete', args=(context['contact'].pk,))

        context['associated_projects_table'] = table_project.ProjectAssocAjaxTable( get_tiered_proj_assoc_qs(self.object) )
        context['associated_tasks_table'] = table_task.TaskAssocAjaxTable( get_tiered_task_assoc_qs(self.object) )
        context['associated_events_table'] = table_event.EventTable_Basic( self.object.events.get_queryset() )

        context['project_source'] = 'data-contact-project'
        context['event_source'] = 'data-contact-event'
        context['task_source'] = 'data-contact-task'

        context['given_pk'] = context['contact'].pk

        return context

class ContactCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'contacts/contact_form.html'
    form_class = ContactForm
    model = Contact

    permission_required = 'contact.add_contact'

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

class ContactUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'contacts/contact_form.html'
    form_class = ContactForm
    model = Contact

    permission_required = 'contact.change_contact'

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

class ContactDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts')
    model = Contact

    permission_required = 'contact.delete_contact'

#___  ____ _ _ _ _  _ _    ____ ____ ___  ____ 
#|  \ |  | | | | |\ | |    |  | |__| |  \ [__  
#|__/ |__| |_|_| | \| |___ |__| |  | |__/ ___] 
#
@permission_required('contact.contact_down_sum_all')
def download_contact_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.get_queryset())

    response.write(contact_set.export('xlsx'))
    return response

@permission_required('contact.contact_down_sum_all')
def download_contact_volunteer_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_volunteer_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['vo']))

    response.write(contact_set.export('xlsx'))
    return response

@permission_required('contact.contact_down_sum_all')
def download_contact_prospect_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_prospect_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['pr']))

    response.write(contact_set.export('xlsx'))
    return response


@permission_required('contact.contact_down_sum_all')
def download_contact_donor_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_donor_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['do']))

    response.write(contact_set.export('xlsx'))
    return response

@permission_required('contact.contact_down_sum_all')
def download_contact_grant_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_grant_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['_g']))

    response.write(contact_set.export('xlsx'))
    return response

@permission_required('contact.contact_down_sum_all')
def download_contact_corporation_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_corporation_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['_f']))

    response.write(contact_set.export('xlsx'))
    return response

class ContactPrintView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_printable.html'

    def test_func(self):
        if self.request.user.has_perm("contact.contact_view_all"):
            return True
        elif self.request.user.has_perm("contact.contact_view_related"):
            this = Contact.objects.get(pk=self.kwargs['pk'])
            return is_related_contact(self.request.user.contact, this)
        return False

    def get_context_data(self, **kwargs):
        context = super(ContactPrintView, self).get_context_data(**kwargs)

        context['associated_projects_table'] = table_assoc.ProjectAssocTable_Printable( self.object.proj_assocs.get_queryset() )
        context['associated_tasks_table'] = table_assoc.TaskAssocTable_Printable( self.object.task_assocs.get_queryset() )
        context['associated_events_table'] = table_event.EventTable_Printable( self.object.events.get_queryset() )

        return context