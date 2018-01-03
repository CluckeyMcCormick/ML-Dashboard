from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

        user_con = self.request.user.contact
        context['my_project_table'] = table_assoc.ProjCon_Project_Table(user_con.proj_assocs.exclude(tag_type__exact='re'))

        return context

class ProjAssoc_AddView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'assign/assign_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjAssoc_AddView, self).get_context_data(**kwargs)

        context['con_que'] = Contact.objects.exclude(projects__pk__in=[ kwargs['pk'] ])

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
