from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic

import datetime
import re

from ..models import Contact, Project, ProjectContactAssoc

from ..forms import ProjectForm

from ..tables import (
    assoc_tables        as table_assoc,
    project_tables      as table_proj,
    task_tables         as table_task,
    custom_tables       as table_custom
)

from ..reports import get_project_dataset, get_project_summary

#Is the provided contact related to proj?
def is_related_contact(con, proj):
    #Is this contact assigned to this project?
    proj_assign_que = Project.objects.filter(pk__exact=proj.pk, contacts__in=[con], con_assocs__tag_type__in=['cr', 'as', 'le'])

    return proj_assign_que.exists()

#Is the provided contact admin role of provided task?
def is_admined_contact_proj(con, proj):
    #Is this contact an admin to this project?
    proj_assign_que = Project.objects.filter(pk__exact=proj.pk, contacts__in=[con], con_assocs__tag_type__in=['cr', 'le'])

    return proj_assign_que.exists()

#___  ____ ____  _ ____ ____ ___    _  _ _ ____ _ _ _ ____ 
#|__] |__/ |  |  | |___ |     |     |  | | |___ | | | [__  
#|    |  \ |__| _| |___ |___  |      \/  | |___ |_|_| ___] 
#                                                          
class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'

    permission_required = 'contact.project_view_all'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        context['project_table'] = table_proj.ProjectTable()
        context['download_all_url'] = reverse_lazy('projects-all-download')
        context['download_incomplete_url'] = reverse_lazy('projects-incomplete-download')
        return context

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def test_func(self):
        if self.request.user.has_perm("contact.project_view_all"):
            return True
        elif self.request.user.has_perm("contact.project_view_related"):
            this = Project.objects.get(pk=self.kwargs['pk'])
            return is_related_contact(self.request.user.contact, this)
        return False

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        context['project_edit_url'] = reverse_lazy('project-update', args=(context['project'].pk,))
        context['project_delete_url'] = reverse_lazy('project-delete', args=(context['project'].pk,))
        context['project_print_url'] = reverse_lazy('project-print', args=(context['project'].pk,))

        context['project_add_lead_url'] = reverse_lazy('project-add-lead', args=(context['project'].pk,))
        context['project_add_assign_url'] = reverse_lazy('project-add-volunteer', args=(context['project'].pk,))
        context['project_add_resource_url'] = reverse_lazy('project-add-resource', args=(context['project'].pk,))

        context['new_project_task_url'] = reverse_lazy('task-project-create', args=(context['project'].pk,))

        con_assoc_qs = self.object.con_assocs.exclude(tag_type='cr')

        context['associated_contact_table'] = table_assoc.ContactProjectTable( con_assoc_qs )
        context['associated_task_table'] = table_task.TaskNoProjectTable(self.object.tasks.get_queryset())

        intersection_data = self.object.contacts.union( Contact.objects.filter(tasks__in=self.object.tasks.get_queryset()) )

        context['contact_task_intersect_table'] = table_custom.ProjectContactIntersection(
            data=intersection_data.distinct(),
            in_query=self.object.tasks.get_queryset(),
            project=self.object
        )

        context['creator'] = None
        ob_con_que = self.object.con_assocs.filter(tag_type='cr')
        if ob_con_que.exists():
            context['creator'] = ob_con_que[0]
            
        context['can_download'] = False
        if self.request.user.has_perm("contact.project_down_sum_each"):
            context['can_download'] = True
        elif self.request.user.has_perm("contact.project_down_sum_related"):
            context['can_download'] = is_related_contact(self.request.user.contact, self.object)

        context['can_edit'] = False
        if self.request.user.has_perm("contact.change_project"):
            context['can_edit'] = True
        elif self.request.user.has_perm("contact.project_change_admin"):
            context['can_edit'] = is_admined_contact_proj(self.request.user.contact, self.object)

        context['can_delete'] = False
        if self.request.user.has_perm("contact.delete_project"):
            context['can_delete'] = True
        elif self.request.user.has_perm("contact.project_delete_admin"):
            context['can_delete'] = is_admined_contact_proj(self.request.user.contact, self.object)

        context['can_assign'] = False
        if self.request.user.has_perm("contact.project_assign"):
            context['can_assign'] = True
        elif self.request.user.has_perm("contact.project_assign_admin"):
            context['can_assign'] = is_admined_contact_proj(self.request.user.contact, self.object)
        
        if context['can_assign']:    
            context['associated_contact_table'] = table_assoc.ContactProjectTable_Remove( con_assoc_qs )

        context['can_add_task'] = False
        if self.request.user.has_perm("contact.task_add_to"):
            context['can_add_task'] = True
        elif self.request.user.has_perm("contact.task_add_admin"):
            context['can_add_task'] = is_admined_contact_proj(self.request.user.contact, self.object)

        return context

    def post(self, *args, **kwargs):
        proj_inst = get_object_or_404(Project, pk=kwargs['pk'])
        user = self.request.user.contact

        if ('mark' in self.request.POST) and is_related_contact(user, proj_inst):
            proj_inst.complete = self.request.POST['mark']
            proj_inst.save()

        elif ('assoc_id' in self.request.POST) and is_admined_contact_proj(user, proj_inst):
            assoc_inst = get_object_or_404(ProjectContactAssoc, pk=self.request.POST['assoc_id'])
            assoc_inst.delete()

        return HttpResponseRedirect( reverse_lazy( 'project-detail', args=(kwargs['pk'],) ) )

class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    model = Project

    permission_required = 'contact.add_project'

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

class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    model = Project

    def test_func(self):
        if self.request.user.has_perm("contact.change_project"):
            return True
        elif self.request.user.has_perm("contact.project_change_admin"):
            this = Project.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_proj(self.request.user.contact, this)
        return False

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

class ProjectDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects')
    model = Project

    def test_func(self):
        if self.request.user.has_perm("contact.delete_project"):
            return True
        elif self.request.user.has_perm("contact.project_delete_admin"):
            this = Project.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_proj(self.request.user.contact, this)
        return False

#___  ____ _ _ _ _  _ _    ____ ____ ___  ____ 
#|  \ |  | | | | |\ | |    |  | |__| |  \ [__  
#|__/ |__| |_|_| | \| |___ |__| |  | |__/ ___] 
#
@permission_required('contact.project_down_sum_all')
def download_project_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="project_list_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    proj_set = get_project_dataset(Project.objects.get_queryset())

    response.write(proj_set.export('xlsx'))
    return response

@permission_required('contact.project_down_sum_all')
def download_project_incomplete_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="project_list_incomplete_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    proj_set = get_project_dataset(Project.objects.filter(complete__exact=False))

    response.write(proj_set.export('xlsx'))
    return response

class ProjectPrintView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_printable.html'

    def test_func(self):
        if self.request.user.has_perm("contact.project_view_all"):
            return True
        elif self.request.user.has_perm("contact.project_view_related"):
            this = Project.objects.get(pk=self.kwargs['pk'])
            return is_related_contact(self.request.user.contact, this)
        return False

    def get_context_data(self, **kwargs):
        context = super(ProjectPrintView, self).get_context_data(**kwargs)

        con_assoc_qs = context['project'].con_assocs.exclude(tag_type='cr')

        context['associated_contact_table'] = table_assoc.ContactProjectTable_Printable( 
            con_assoc_qs, 
        )

        context['associated_task_table'] = table_task.TaskNoProjectTable_Printable(
            context['project'].tasks.get_queryset(), 
        )

        intersection_data = context['project'].contacts.union( Contact.objects.filter(tasks__in=context['project'].tasks.get_queryset()) )

        context['contact_task_intersect_table'] = table_custom.PCI_Table_Printable(
            data=intersection_data.distinct(),
            in_query=context['project'].tasks.get_queryset(),
            project=context['project'],
        )

        context['creator'] = None
        ob_con_que = context['project'].con_assocs.filter(tag_type='cr')
        if ob_con_que.exists():
            context['creator'] = ob_con_que.first()

        return context


