from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from ..models import Organization, Contact

from ..forms import OrgForm

from ..tables import (
    contact_tables      as table_con,
    organization_tables as table_org,
) 

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

