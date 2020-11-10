from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import generic

from ..models import Contact, Project, ProjectContactAssoc

from ..tables import (
    assoc_tables   as table_assoc,
    contact_tables as table_con,
    project_tables as table_proj
) 

from .project_views import is_admined_contact_proj

def get_tiered_proj_assoc_qs(user_con):
    user_projects = user_con.projects.get_queryset()
    # Get all of the project associations
    ua_all = user_con.proj_assocs.get_queryset()
    # We only want projects where we're assigned, a leader, or a creator
    ua_filtered = ua_all.filter(tag_type__in=['as', 'le', 'cr'])
    # Get all the ones where we're assigned or a leader
    ua_assign = ua_filtered.filter(tag_type__in=['as', 'le'])
    # Get ones where we're the creator
    ua_create = ua_filtered.filter(tag_type__in=['cr'])    

    #Now, get those tasks that have an assigned relation
    #and those that have a creator relation
    assigned_projects = user_projects.filter(con_assocs__in=ua_assign)
    created_projects = user_projects.filter(con_assocs__in=ua_create)

    # Now, get the projects that ARE assigned to us AND we've created.
    projects_created_assigned = created_projects.filter(id__in=assigned_projects)

    # Exclude any creator tags that have projects for assigned or leader roles
    return ua_filtered.exclude(tag_type__in=['cr'], proj__in=projects_created_assigned)

#___  ____ ____  _ ____ ____ ___    ____ ____ ____ ____ ____ 
#|__] |__/ |  |  | |___ |     |     |__| [__  [__  |  | |    
#|    |  \ |__| _| |___ |___  |     |  | ___] ___] |__| |___ 
#                                                            
#_  _ _ ____ _ _ _ ____ 
#|  | | |___ | | | [__  
# \/  | |___ |_|_| ___] 
#                       
class MyProjectView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'proj_con_assocs/my_assoc_proj.html'

    def get_context_data(self, **kwargs):
        context = super(MyProjectView, self).get_context_data(**kwargs)

        assoc_que = get_tiered_proj_assoc_qs( self.request.user.contact )
        context['my_project_table'] = table_proj.ProjectAssocAjaxTable( assoc_que )

        context['source_name'] = 'data-dashboard-project'
        context['input_id'] = self.request.user.contact.pk
        
        return context

class ProjAssoc_AddView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'assign/assign_form.html'

    def test_func(self):
        if self.request.user.has_perm("contact.task_assign"):
            return True
        elif self.request.user.has_perm("contact.task_assign_admin"):
            task = Task.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_proj(self.request.user.contact, task)
        return False

    def get_context_data(self, **kwargs):
        context = super(ProjAssoc_AddView, self).get_context_data(**kwargs)

        assoc_set = ProjectContactAssoc.objects.filter(proj=kwargs['pk'], tag_type__in=['as', 'le', 're', 'na'])
        context['con_que'] = Contact.objects.exclude(proj_assocs__in=assoc_set)  

        context['assign_table'] = ' '
        context['page_title'] = 'Assign <t style="text-decoration: underline;">{0}</t> -'
        context['item_title'] = Project.objects.get(pk=kwargs['pk']).title
        
        context['input_id'] = kwargs['pk']

        return context        

    def post(self, *args, **kwargs):

        proj_inst = get_object_or_404(Project, pk=kwargs['pk'])
        con_inst = get_object_or_404(Contact, pk=args[0].POST[ kwargs['target_key'] ])

        new_assoc = ProjectContactAssoc(proj=proj_inst, con=con_inst, tag_type=kwargs['tag_type'])
        new_assoc.save()

        return HttpResponseRedirect( reverse_lazy( 'project-detail', args=(kwargs['pk'],) ) )

class ProjectAssoc_AssignView(ProjAssoc_AddView):

    def get_context_data(self, **kwargs):
        context = super(ProjectAssoc_AssignView, self).get_context_data(**kwargs)

        context['con_que'] = context['con_que'].filter(tags__tag_type__in=['vo'])

        context['assign_table'] = table_con.SelectVolunteerTable( context['con_que'] )
        context['page_title'] = mark_safe( context['page_title'].format('Volunteer') )

        context['source_name'] = 'data-project-assign'

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 'as'
        kwargs['target_key'] = 'vol_id'

        return super(ProjectAssoc_AssignView, self).post(*args, **kwargs)

class ProjectAssoc_LeadView(ProjAssoc_AddView):

    def get_context_data(self, **kwargs):
        context = super(ProjectAssoc_LeadView, self).get_context_data(**kwargs)

        context['con_que'] = context['con_que'].filter(tags__tag_type__in=['vo'])

        context['assign_table'] = table_con.SelectLeadTable( context['con_que'] )
        context['page_title'] = mark_safe( context['page_title'].format('Lead') )

        context['source_name'] = 'data-project-lead'

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 'le'
        kwargs['target_key'] = 'lead_id'

        return super(ProjectAssoc_LeadView, self).post(*args, **kwargs)

class ProjectAssoc_ResourceView(ProjAssoc_AddView):

    def get_context_data(self, **kwargs):
        context = super(ProjectAssoc_ResourceView, self).get_context_data(**kwargs)

        context['assign_table'] = table_con.SelectResourceTable( context['con_que'] )
        context['page_title'] = mark_safe( context['page_title'].format('Resource') )

        context['source_name'] = 'data-project-resource'

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 're'
        kwargs['target_key'] = 'res_id'

        return super(ProjectAssoc_ResourceView, self).post(*args, **kwargs)
