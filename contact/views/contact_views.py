from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

import datetime

from ..reports import get_contact_dataset

from ..models import ContactTypeTag, Contact

from ..forms import ContactForm

from ..tables import (
    assoc_tables        as table_assoc,
    contact_tables      as table_con,
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

        context['download_all_url'] = reverse_lazy('contacts-all-download')
        context['download_volunteer_url'] = reverse_lazy('contacts-volunteer-download')
        context['download_prospect_url'] = reverse_lazy('contacts-prospect-download')
        context['download_donor_url'] = reverse_lazy('contacts-donor-download')
        context['download_grant_url'] = reverse_lazy('contacts-grant-download')
        context['download_corporation_url'] = reverse_lazy('contacts-corporation-download')

        return context

def download_contact_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.get_queryset())

    response.write(contact_set.export('xlsx'))
    return response

def download_contact_volunteer_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_volunteer_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['vo']))

    response.write(contact_set.export('xlsx'))
    return response

def download_contact_prospect_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_prospect_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['pr']))

    response.write(contact_set.export('xlsx'))
    return response

def download_contact_donor_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_donor_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['do']))

    response.write(contact_set.export('xlsx'))
    return response

def download_contact_grant_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_grant_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['_g']))

    response.write(contact_set.export('xlsx'))
    return response

def download_contact_corporation_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="contact_list_corporation_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    contact_set = get_contact_dataset(Contact.objects.filter(tags__tag_type__in=['_f']))

    response.write(contact_set.export('xlsx'))
    return response

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
