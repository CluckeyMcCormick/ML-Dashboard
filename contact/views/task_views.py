from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

import datetime
import re

from ..reports import get_task_dataset, get_task_summary

from ..models import Task, TaskContactAssoc, Contact

from ..forms import TaskForm

from ..tables import (
    assoc_tables        as table_assoc,
    task_tables         as table_task
) 

#___ ____ ____ _  _    _  _ _ ____ _ _ _ ____ 
# |  |__| [__  |_/     |  | | |___ | | | [__  
# |  |  | ___] | \_     \/  | |___ |_|_| ___] 
#                                             
class TaskListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['task_table'] = table_task.TaskTable()

        context['download_all_url'] = reverse_lazy('tasks-all-download')
        context['download_incomplete_url'] = reverse_lazy('tasks-incomplete-download')

        return context


def download_task_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="task_list_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    task_set = get_task_dataset(Task.objects.get_queryset())

    response.write(task_set.export('xlsx'))
    return response

def download_task_incomplete_dataset(request):
    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="task_list_incomplete_{0}.xlsx"'.format(current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    task_set = get_task_dataset(Task.objects.filter(complete__exact=False))

    response.write(task_set.export('xlsx'))
    return response


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)

        context['edit_url'] = reverse_lazy('task-update', args=(context['task'].pk,))
        context['delete_url'] = reverse_lazy('task-delete', args=(context['task'].pk,))

        context['task_download_url'] = reverse_lazy('task-download', args=(context['task'].pk,))

        context['add_volunteer_url'] = reverse_lazy('task-add-volunteer', args=(context['task'].pk,))
        context['add_target_url'] = reverse_lazy('task-add-target', args=(context['task'].pk,))
        context['add_resource_url'] = reverse_lazy('task-add-resource', args=(context['task'].pk,))

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

def download_task_summary(request, pk=None):
    task = Task.objects.get(pk=pk)

    normal_title = re.sub( r"[,-.?!/\\]", '', task.brief.lower() ).replace(' ','_')

    current_str = datetime.date.today().strftime('%Y_%m_%d')

    dispose = 'attachment; filename="{0}_{1}.xlsx"'.format(normal_title, current_str)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = dispose

    task_sum = get_task_summary(pk)

    response.write(task_sum.export('xlsx'))

    return response

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

class TaskUnboundCreate(TaskCreate):

    def get_form(self):
        form = super(TaskUnboundCreate, self).get_form()

        form.fields['proj'].disabled = True

        return form

class TaskProjectCreate(TaskUnboundCreate):

    def get_initial(self):
        initial = super(TaskUnboundCreate, self).get_initial()
        initial['proj'] = self.kwargs['pk']

        return initial

    def get_context_data(self, **kwargs):
        context = super(TaskProjectCreate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_bound'] = True

        return context

class TaskUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    model = Task

    def get_initial(self):
        initial = super(TaskUpdate, self).get_initial()

        id_query = TaskContactAssoc.objects.filter(task__exact=self.object.pk, tag_type__in=['as','ta'])

        assigned_query = Contact.objects.filter(task_assocs__in=id_query.filter(tag_type__exact='as'))
        target_query = Contact.objects.filter(task_assocs__in=id_query.filter(tag_type__exact='ta'))

        initial['volunteers'] = []
        initial['targets'] = []

        for vol_val in assigned_query.values_list('id', flat=True):
            initial['volunteers'].append(vol_val)

        for tar_val in target_query.values_list('id', flat=True):
            initial['targets'].append(tar_val)

        return initial

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)

        #Get the tasks associated with the user
        context['is_create'] = False

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_task = form.save()
        
        form.handle_task_assignments(new_task)

        return HttpResponseRedirect(reverse_lazy('task-detail', args=(new_task.pk,)))

class TaskDelete(LoginRequiredMixin, DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    model = Task
