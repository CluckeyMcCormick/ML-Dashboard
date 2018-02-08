from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import generic

from ..models import Event, Contact

from ..forms import EventForm

from ..tables import (
    contact_tables as table_con,
    event_tables   as table_event,
) 

#____ _  _ ____ _  _ ___    _  _ _ ____ _ _ _ ____ 
#|___ |  | |___ |\ |  |     |  | | |___ | | | [__  
#|___  \/  |___ | \|  |      \/  | |___ |_|_| ___]                                                  
#
class EventListView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'events/event_list.html'

    permission_required = 'contact.event_view_all'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)

        context['event_table'] = table_event.EventTable()

        return context

class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    permission_required = 'contact.event_view_all'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)

        context['event_print_url'] = reverse_lazy('event-print', args=(context['event'].pk,))
        context['event_edit_url'] = reverse_lazy('event-update', args=(context['event'].pk,))
        context['event_delete_url'] = reverse_lazy('event-delete', args=(context['event'].pk,))
        context['associated_contact_table'] = table_con.ContactOrglessTable( Contact.objects.filter(events__in=[self.object]) ) 

        return context

class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    form_class = EventForm
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
    template_name = 'events/event_form.html'
    form_class = EventForm
    success_url = reverse_lazy('event-detail')

    permission_required = 'contact.change_event'

    def form_valid(self, form):
        updated_event = form.save()       
        return HttpResponseRedirect(reverse_lazy('event-detail', args=(updated_event.pk,)))

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events')

    permission_required = 'contact.delete_event'

class EventPrintView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'events/event_printable.html'

    permission_required = 'contact.event_view_all'

    def get_context_data(self, **kwargs):
        context = super(EventPrintView, self).get_context_data(**kwargs)

        context['associated_contact_table'] = table_con.ContactOrglessTable_Printable( Contact.objects.filter(events__in=[self.object]) ) 

        return context