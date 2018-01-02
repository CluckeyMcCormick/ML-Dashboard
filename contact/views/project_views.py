from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from ..models import Project, ProjectContactAssoc

from ..forms import ProjectForm

from ..tables import (
    assoc_tables        as table_assoc,
    project_tables      as table_proj,
    task_tables         as table_task
) 

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

        context['project_add_lead_url'] = reverse_lazy('project-add-lead', args=(context['project'].pk,))
        context['project_add_assign_url'] = reverse_lazy('project-add-volunteer', args=(context['project'].pk,))
        context['project_add_resource_url'] = reverse_lazy('project-add-resource', args=(context['project'].pk,))

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

