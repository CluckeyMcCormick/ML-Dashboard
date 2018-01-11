from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

import datetime
import re

from ..reports import get_task_dataset, get_task_summary

from ..models import Task, TaskContactAssoc, Contact, Project

from ..forms import TaskForm

from ..tables import (
    assoc_tables        as table_assoc,
    task_tables         as table_task
) 

#Is the provided contact related to task?
def is_related_contact(con, task):
    #Is this contact assigned to this task?
    task_assign_que = Task.objects.filter(pk__exact=task.pk, contacts__in=[con], con_assocs__tag_type__in=['cr', 'as'])

    #Is this contact assigned to the task's project?
    proj_assign_que = Task.objects.filter(pk__exact=task.pk, proj__contacts__in=[con], proj__con_assocs__tag_type__in=['cr', 'as', 'le'])

    return task_assign_que.exists() or proj_assign_que.exists()

#Is the provided contact admin role of provided task?
def is_admined_contact_task(con, task):
    #Is this contact assigned to this task?
    task_assign_que = Task.objects.filter(pk__exact=task.pk, contacts__in=[con], con_assocs__tag_type__in=['cr'])

    #Is this contact assigned to the task's project?
    proj_assign_que = Task.objects.filter(pk__exact=task.pk, proj__contacts__in=[con], proj__con_assocs__tag_type__in=['cr', 'le'])

    return task_assign_que.exists() or proj_assign_que.exists()

#Is the provided contact admin role of provided project?
def is_admined_contact_project(con, proj):

    #Is this contact assigned to the task's project?
    proj_assign_que = Proj.objects.filter(pk__exact=proj.pk, contacts__in=[con], con_assocs__tag_type__in=['cr', 'le'])

    return proj_assign_que.exists()

#___ ____ ____ _  _    _  _ _ ____ _ _ _ ____ 
# |  |__| [__  |_/     |  | | |___ | | | [__  
# |  |  | ___] | \_     \/  | |___ |_|_| ___] 
#                                             
class TaskListView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'tasks/task_list.html'

    permission_required = 'contact.task_view_all'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['task_table'] = table_task.TaskTable()

        context['download_all_url'] = reverse_lazy('tasks-all-download')
        context['download_incomplete_url'] = reverse_lazy('tasks-incomplete-download')

        return context

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def test_func(self):
        if self.request.user.has_perm("contact.task_view_all"):
            return True
        elif self.request.user.has_perm("contact.task_view_related"):
            this = Task.objects.get(pk=self.kwargs['pk'])
            return is_related_contact(self.request.user.contact, this)
        return False

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)

        context['edit_url'] = reverse_lazy('task-update', args=(context['task'].pk,))
        context['delete_url'] = reverse_lazy('task-delete', args=(context['task'].pk,))

        context['task_download_url'] = reverse_lazy('task-download', args=(context['task'].pk,))

        context['add_volunteer_url'] = reverse_lazy('task-add-volunteer', args=(context['task'].pk,))
        context['add_target_url'] = reverse_lazy('task-add-target', args=(context['task'].pk,))
        context['add_resource_url'] = reverse_lazy('task-add-resource', args=(context['task'].pk,))

        context['associated_contact_table'] = table_assoc.TaskCon_Contact_Table( self.object.con_assocs.get_queryset() )

        context['can_download'] = False
        if self.request.user.has_perm("contact.task_down_sum_each"):
            context['can_download'] = True
        elif self.request.user.has_perm("contact.task_down_sum_related"):
            context['can_download'] = is_related_contact(self.request.user.contact, self.object)

        context['can_edit'] = False
        if self.request.user.has_perm("contact.change_task"):
            context['can_edit'] = True
        elif self.request.user.has_perm("contact.task_change_admin"):
            context['can_edit'] = is_admined_contact_task(self.request.user.contact, self.object)

        context['can_delete'] = False
        if self.request.user.has_perm("contact.delete_task"):
            context['can_delete'] = True
        elif self.request.user.has_perm("contact.task_delete_admin"):
            context['can_delete'] = is_admined_contact_task(self.request.user.contact, self.object)

        context['can_assign'] = False
        if self.request.user.has_perm("contact.task_assign"):
            context['can_assign'] = True
            context['associated_contact_table'] = table_assoc.TaskCon_ContactRemove_Table( self.object.con_assocs.get_queryset() )
        elif self.request.user.has_perm("contact.task_assign_admin"):
            context['can_assign'] = is_admined_contact_task(self.request.user.contact, self.object)
            context['associated_contact_table'] = table_assoc.TaskCon_ContactRemove_Table( self.object.con_assocs.get_queryset() )

        return context

    def post(self, *args, **kwargs):

        if 'mark' in self.request.POST:
            task_inst = get_object_or_404(Task, pk=kwargs['pk'])
            task_inst.complete = self.request.POST['mark']
            task_inst.save()

        elif 'assoc_id' in self.request.POST:
            assoc_inst = get_object_or_404(TaskContactAssoc, pk=self.request.POST['assoc_id'])
            assoc_inst.delete()

        return HttpResponseRedirect( reverse_lazy( 'task-detail', args=(kwargs['pk'],) ) )

class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = True

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_task = form.save()
        
        creator_assoc = TaskContactAssoc(con=self.request.user.contact, task=new_task, tag_type='cr')
        creator_assoc.save()

        return HttpResponseRedirect(reverse_lazy('task-detail', args=(new_task.pk,)))

class TaskUnboundCreate(TaskCreate, PermissionRequiredMixin):

    permission_required = 'contact.add_task'

    def get_form(self):
        form = super(TaskUnboundCreate, self).get_form()

        form.fields['proj'].disabled = True

        return form

class TaskProjectCreate(TaskCreate, UserPassesTestMixin):

    def test_func(self):
        if self.request.user.has_perm("contact.add_task"):
            return True
        elif self.request.user.has_perm("contact.task_add_admin"):
            proj = Project.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_project(self.request.user.contact, proj)
        return False


    def get_form(self):
        form = super(TaskProjectCreate, self).get_form()

        form.fields['proj'].disabled = True

        return form

    def get_initial(self):
        initial = super(TaskUnboundCreate, self).get_initial()
        initial['proj'] = self.kwargs['pk']

        return initial

    def get_context_data(self, **kwargs):
        context = super(TaskProjectCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_bound'] = True

        return context

class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    model = Task

    def test_func(self):
        if self.request.user.has_perm("contact.change_task"):
            return True
        elif self.request.user.has_perm("contact.task_change_admin"):
            task = Task.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_task(self.request.user.contact, task)
        return False

    def get_form(self):
        form = super(TaskUpdate, self).get_form()

        form.fields['proj'].disabled = True

        return form

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = False

        return context

class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    model = Task

    def test_func(self):
        if self.request.user.has_perm("contact.delete_task"):
            return True
        elif self.request.user.has_perm("contact.task_delete_admin"):
            task = Task.objects.get(pk=self.kwargs['pk'])
            return is_admined_contact_task(self.request.user.contact, task)
        return False

#___  ____ _ _ _ _  _ _    ____ ____ ___  ____ 
#|  \ |  | | | | |\ | |    |  | |__| |  \ [__  
#|__/ |__| |_|_| | \| |___ |__| |  | |__/ ___] 
#
@permission_required('contact.task_down_sum_all')
def download_task_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="task_list_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    task_set = get_task_dataset(Task.objects.get_queryset())

    response.write(task_set.export('xlsx'))
    return response

@permission_required('contact.task_down_sum_all')
def download_task_incomplete_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="task_list_incomplete_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    task_set = get_task_dataset(Task.objects.filter(complete__exact=False))

    response.write(task_set.export('xlsx'))
    return response

def download_task_summary(request, pk=None):
    task = Task.objects.get(pk=pk)

    if not ( \
        (is_related_contact(request.user.contact, task) and \
        request.user.has_perm("contact.task_down_sum_related") \
    ) \
    or request.user.has_perm("contact.task_down_sum_each") ):
        return redirect('/accounts/login/?next=%s' % request.path)

    normal_title = re.sub( r"[,-.?!/\\]", '', task.brief.lower() ).replace(' ','_')

    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="{0}_{1}.xlsx"'.format(normal_title, current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    task_sum = get_task_summary(pk)

    response.write(task_sum.export('xlsx'))

    return response