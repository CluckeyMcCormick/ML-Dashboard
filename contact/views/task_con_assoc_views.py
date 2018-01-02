from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import generic

from ..models import Contact, Task, TaskContactAssoc

from ..tables import (
    assoc_tables as table_assoc,
) 

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

        user_con = self.request.user.contact
        context['my_task_table'] = table_assoc.TaskCon_Task_Table(user_con.task_assocs.exclude(tag_type__exact='ta'))

        return context
