from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import generic

from ..models import Event, Contact

from ..forms import OrgForm

from ..tables import (
    contact_tables      as table_con,
    organization_tables as table_org,
) 

#____ ____ ____ ____ _  _ _ ___  ____ ___ _ ____ _  _    _  _ _ ____ _ _ _ ____ 
#|  | |__/ | __ |__| |\ | |   /  |__|  |  | |  | |\ |    |  | | |___ | | | [__  
#|__| |  \ |__] |  | | \| |  /__ |  |  |  | |__| | \|     \/  | |___ |_|_| ___] 
#
class EventListView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'organizations/org_list.html'

    permission_required = 'contact.event_view_all'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)

        context['org_table'] = table_org.OrgTable()

        return context

class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'organizations/org_detail.html'

    permission_required = 'contact.event_view_all'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)

        context['org_print_url'] = reverse_lazy('org-print', args=(context['organization'].pk,))
        context['org_edit_url'] = reverse_lazy('org-update', args=(context['organization'].pk,))
        context['org_delete_url'] = reverse_lazy('org-delete', args=(context['organization'].pk,))
        context['associated_contact_table'] = table_con.ContactOrglessTable( Contact.objects.filter(org__exact=self.object) ) 

        return context

class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'organizations/org_form.html'
    form_class = OrgForm
    success_url = reverse_lazy('event-detail')

    permission_required = 'contact.add_event'

    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

    def form_valid(self, form):
        new_event = form.save()       
        return HttpResponseRedirect(reverse_lazy('event-detail', args=(new_event.pk,)))

class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    template_name = 'organizations/org_form.html'
    form_class = OrgForm
    success_url = reverse_lazy('event-detail')

    permission_required = 'contact.change_event'

    def form_valid(self, form):
        updated_event = form.save()       
        return HttpResponseRedirect(reverse_lazy('event-detail', args=(updated_event.pk,)))

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'organizations/org_confirm_delete.html'
    success_url = reverse_lazy('events')

    permission_required = 'contact.delete_event'

class EventPrintView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'organizations/org_printable.html'

    permission_required = 'contact.event_view_all'

    def get_context_data(self, **kwargs):
        context = super(EventPrintView, self).get_context_data(**kwargs)

        context['associated_contact_table'] = table_con.ContactOrglessTable_Printable( Contact.objects.filter(org__exact=self.object) ) 

        return context