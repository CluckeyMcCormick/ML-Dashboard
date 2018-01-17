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
) 

from .project_views import is_admined_contact_proj

def get_tiered_proj_assoc_qs(user_con):
    user_projects = user_con.projects.get_queryset()

    ua_all = user_con.proj_assocs.get_queryset()
    ua_assign = ua_all.filter(tag_type__in=['as', 'le'])
    ua_create = ua_all.filter(tag_type__in=['cr'])

    #Now, get those tasks that have an assigned relation
    #and those that have a creator relation
    assigned_projects = user_projects.filter(con_assocs__in=ua_assign)
    created_projects = user_projects.filter(con_assocs__in=ua_create)

    #Now, get the projects that AREN'T assigned 
    #Which means, only getting the projects we've created
    #And some others we don't really care about
    projects_no_assigned = user_projects.exclude(id__in=assigned_projects)

    #Now, we take all our creator associations, and limit it to
    #ONLY the ones that have no ASSIGN relation
    ua_create = ua_create.filter(proj__in=projects_no_assigned)

    return ua_assign.union(ua_create)

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
        context['my_project_table'] = table_assoc.ProjCon_Project_Table( assoc_que )

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

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 're'
        kwargs['target_key'] = 'res_id'

        return super(ProjectAssoc_ResourceView, self).post(*args, **kwargs)
