
from django.template import loader
from django.http import HttpResponse

import tablib

from .models import (
    Project, ProjectContactAssoc, 
    Task, TaskContactAssoc
)

def get_contact_dataset(query_set):
    vis_headers = [
        "Name", "Email", "Phone Number", "Organization",
        "Is Volunteer?", "Is Prospect?", "Is Donor?", 
        "Is Grant Resource?", "Is Corporation/Foundation?"
    ] 

    data = tablib.Dataset(headers=vis_headers)
    
    for con in query_set:
        if con.org:
            org_name = con.org.name
        else:
            org_name = None

        data.append((
            con.name, con.email, con.phone, org_name,
            con.is_volunteer, con.is_prospect, con.is_donor,
            con.is_resource, con.is_foundation
        ))

    return data

def get_project_dataset(query_set):
    vis_headers = [
        "Title", "Deadline", "Status", "Completion", "Notes"
    ] 

    data = tablib.Dataset(headers=vis_headers)
    
    for proj in query_set:
        data.append( 
            (proj.title, proj.deadline, proj.status, 
            proj.percentage_formatted(), proj.notes) 
        )

    return data

def get_task_dataset(query_set):
    vis_headers = [
        "Brief", "Deadline", "Status", "Project"
    ] 

    data = tablib.Dataset(headers=vis_headers)
    
    for task in query_set:
        if task.proj:
            proj_name = task.proj.title
        else:
            proj_name = None
        data.append( (task.brief, task.deadline, task.status, proj_name) )

    return data

def get_con_assoc_dataset(query_set):
    vis_headers = ["Name", "Role", "Phone", "Email"] 

    data = tablib.Dataset(headers=vis_headers)
    
    for assoc in query_set:
        data.append( (assoc.con.name, assoc.get_tag_type_display(), assoc.con.phone, assoc.con.email ) )

    return data

"""
The summary functions!

Each returns a databook, filled with datasets of pertinent information.
"""
"""
Returns two datasets:
    task data
    assoc contact listing
"""
def get_task_summary_unwrapped(task_pk):
    vis_headers = [
        "Brief", "Deadline", "Status", "Notes", "Project"
    ] 

    task_data = tablib.Dataset(headers=vis_headers)
    
    task = Task.objects.get(pk=task_pk)

    if task.proj:
        proj_name = task.proj.title
    else:
        proj_name = None

    task_data.append( 
        (task.brief, task.deadline, task.status, task.notes, proj_name) 
    )

    assoc_data = get_con_assoc_dataset(TaskContactAssoc.objects.filter(task__exact=task_pk))

    return task_data, assoc_data

"""
Returns a databook listing:
    the project data
    assoc contact listing
    task listing 
    task summaries for each:
        task data
        assoc contact listing
"""
def get_project_summary(project_pk):
    project_data = get_project_dataset(Project.objects.filter(pk__exact=project_pk))
    proj_assoc_data = get_con_assoc_dataset(ProjectContactAssoc.objects.filter(proj__exact=project_pk))

    tasks = Task.objects.filter(proj__exact=project_pk)

    task_list_data = get_task_dataset(tasks)

    book = tablib.Databook( sets=[project_data, proj_assoc_data, task_list_data] )

    for tsk in tasks:
        task_data, assoc_data = get_task_summary_unwrapped(tsk.pk)

        book.add_sheet(task_data)
        book.add_sheet(assoc_data)

    return book

"""
Wraps up our two task datasets into a single book
"""
def get_task_summary(task_pk):
    task_data, assoc_data = get_task_summary_unwrapped(task_pk)
    return tablib.Databook( sets=[task_data, assoc_data] )


