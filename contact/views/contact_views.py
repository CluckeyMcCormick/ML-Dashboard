from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

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
