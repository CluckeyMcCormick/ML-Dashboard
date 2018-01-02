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

@login_required
def project_assign(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    con_que = Contact.objects.exclude(projects__pk__in=[pk]).filter(tags__tag_type__in=['vo'])

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        con_inst=get_object_or_404(Contact, pk=request.POST["vol_id"])
        proj_inst=get_object_or_404(Project, pk=pk)

        new_assoc = ProjectContactAssoc(proj=proj_inst, con=con_inst, tag_type='as')
        new_assoc.save()

        response = HttpResponseRedirect( reverse_lazy( 'project-detail', args=(pk,) ) )
    else:
        context = {}

        context['assign_table'] = table_con.SelectVolunteerTable(con_que)
        context['page_title'] = mark_safe('Assign <t style="text-decoration: underline;">Volunteer</t> -')
        context['item_title'] = Project.objects.get(pk=pk).title

        response = render(request, 'assign/assign_form.html', context)

    return response

@login_required
def project_lead(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    con_que = Contact.objects.exclude(projects__pk__in=[pk]).filter(tags__tag_type__in=['vo'])

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        con_inst=get_object_or_404(Contact, pk=request.POST["lead_id"])
        proj_inst=get_object_or_404(Project, pk=pk)

        new_assoc = ProjectContactAssoc(proj=proj_inst, con=con_inst, tag_type='le')
        new_assoc.save()

        response = HttpResponseRedirect( reverse_lazy( 'project-detail', args=(pk,) ) )

    else:
        context = {}

        context['assign_table'] = table_con.SelectLeadTable(con_que)
        context['page_title'] = mark_safe('Assign <t style="text-decoration: underline;">Volunteer</t> -')
        context['item_title'] = Project.objects.get(pk=pk).title

        response = render(request, 'assign/assign_form.html', context)

    return response

@login_required
def project_resource(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    con_que = Contact.objects.exclude(projects__pk__in=[pk])

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        con_inst=get_object_or_404(Contact, pk=request.POST["res_id"])
        proj_inst=get_object_or_404(Project, pk=pk)

        new_assoc = ProjectContactAssoc(proj=proj_inst, con=con_inst, tag_type='re')
        new_assoc.save()

        response = HttpResponseRedirect( reverse_lazy( 'project-detail', args=(pk,) ) )

    else:
        context = {}

        context['assign_table'] = table_con.SelectResourceTable(con_que)
        context['page_title'] = mark_safe('Add <t style="text-decoration: underline;">Resource</t> -')
        context['item_title'] = Project.objects.get(pk=pk).title

        response = render(request, 'assign/assign_form.html', context)

    return response
