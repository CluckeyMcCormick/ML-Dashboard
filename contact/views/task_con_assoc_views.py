from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import generic

from ..models import Contact, Task, TaskContactAssoc

from ..tables import (
    assoc_tables   as table_assoc,
    contact_tables as table_con
) 

from .task_views import is_admined_contact_task

def get_tiered_task_assoc_qs(user_con):
    user_tasks = user_con.tasks.get_queryset()

    ua_all = user_con.task_assocs.get_queryset()
    ua_assign = ua_all.filter(tag_type__in=['as'])
    ua_create = ua_all.filter(tag_type__in=['cr'])

    #Now, get those tasks that have an assigned relation
    #and those that have a creator relation
    assigned_tasks = user_tasks.filter(con_assocs__in=ua_assign)
    created_tasks = user_tasks.filter(con_assocs__in=ua_create)

    #Now, get the tasks that AREN'T assigned 
    #Which means, only getting the tasks we've created
    #And some others we don't really care about
    tasks_no_assigned = user_tasks.exclude(id__in=assigned_tasks)

    #Now, we take all our creator associations, and limit it to
    #ONLY the ones that have no ASSIGN relation
    ua_create = ua_create.filter(task__in=tasks_no_assigned)

    return ua_assign.union(ua_create)

#___ ____ ____ _  _    ____ ____ _  _    ____ ____ ____ ____ ____ 
# |  |__| [__  |_/  __ |    |  | |\ | __ |__| [__  [__  |  | |    
# |  |  | ___] | \_    |___ |__| | \|    |  | ___] ___] |__| |___ 
#                                                                 
#_  _ _ ____ _ _ _ ____ 
#|  | | |___ | | | [__  
# \/  | |___ |_|_| ___] 
#                       
class MyTaskView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task_con_assocs/my_assoc_task.html'

    def get_context_data(self, **kwargs):
        context = super(MyTaskView, self).get_context_data(**kwargs)

        assoc_que = get_tiered_task_assoc_qs( self.request.user.contact )
        context['my_task_table'] = table_assoc.TaskCon_Task_Table( assoc_que )

        return context

"""
Creates an association between a contact and a task.
This is meant to act as a framework class so that we 
don't have to write any repeat code. 
"""
class TaskAssocAddView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'assign/assign_form.html'

    def test_func(self):
        if self.request.user.has_perm("contact.task_assign"):
            return True
        elif self.request.user.has_perm("contact.task_assign_admin"):
            task = Task.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_task(self.request.user.contact, task)
        return False

    def get_context_data(self, **kwargs):
        context = super(TaskAssocAddView, self).get_context_data(**kwargs)

        assoc_set = TaskContactAssoc.objects.filter(task=kwargs['pk'], tag_type__in=['as', 'ta', 're', 'na'])
        context['con_que'] = Contact.objects.exclude(task_assocs__in=assoc_set)       

        context['assign_table'] = ' '
        context['page_title'] = 'Assign <t style="text-decoration: underline;">{0}</t> -'
        context['item_title'] = Task.objects.get(pk=kwargs['pk']).brief

        return context        

    def post(self, *args, **kwargs):
        task_inst = get_object_or_404(Task, pk=kwargs['pk'])
        con_inst = get_object_or_404(Contact, pk=args[0].POST[ kwargs['target_key'] ])

        new_assoc = TaskContactAssoc(task=task_inst, con=con_inst, tag_type=kwargs['tag_type'])
        new_assoc.save()

        return HttpResponseRedirect( reverse_lazy( 'task-detail', args=(kwargs['pk'],) ) )

"""
Displays a list of contacts.
The one selected will be ASSIGNED to the task.
"""
class TaskAssocAssignView(TaskAssocAddView):

    def get_context_data(self, **kwargs):
        context = super(TaskAssocAssignView, self).get_context_data(**kwargs)

        task_inst=get_object_or_404(Task, pk=kwargs['pk'])
        context['con_que'] = context['con_que'].filter(tags__tag_type__in=['vo'])
        
        if task_inst.proj:
            context['con_que'] = context['con_que'].filter(
                proj_assocs__tag_type__in=['as', 'le', 'cr'], 
                proj_assocs__proj=task_inst.proj
            )

        context['assign_table'] = table_con.SelectVolunteerTable( context['con_que'] )
        context['page_title'] = mark_safe( context['page_title'].format('Volunteer') )

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 'as'
        kwargs['target_key'] = 'vol_id'

        return super(TaskAssocAssignView, self).post(*args, **kwargs)

"""
Displays a list of contacts.
The one selected will be a TARGET for the task.
"""
class TaskAssocTargetView(TaskAssocAddView):

    def get_context_data(self, **kwargs):
        context = super(TaskAssocTargetView, self).get_context_data(**kwargs)

        context['assign_table'] = table_con.SelectTargetTable( context['con_que'] )
        context['page_title'] = mark_safe( context['page_title'].format('Target') )

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 'ta'
        kwargs['target_key'] = 'targ_id'

        return super(TaskAssocTargetView, self).post(*args, **kwargs)

"""
Displays a list of contacts.
The one selected will be a RESOURCE for the task.
"""
class TaskAssocResourceView(TaskAssocAddView):

    def get_context_data(self, **kwargs):
        context = super(TaskAssocResourceView, self).get_context_data(**kwargs)

        context['assign_table'] = table_con.SelectResourceTable( context['con_que'] )
        context['page_title'] = mark_safe( context['page_title'].format('Resource') )

        return context

    def post(self, *args, **kwargs):
        kwargs['tag_type'] = 're'
        kwargs['target_key'] = 'res_id'

        return super(TaskAssocResourceView, self).post(*args, **kwargs)

