from django.contrib.auth.models import Group, Permission

volunteer_group,_ = Group.objects.get_or_create(name='Volunteer')

contact_input_group,_= Group.objects.get_or_create(name='Contact Input Worker')
organization_input_group,_= Group.objects.get_or_create(name='Organization Input Worker')
event_input_group,_= Group.objects.get_or_create(name='Event / Workshop Input Worker')
project_input_group,_= Group.objects.get_or_create(name='Project Input Worker')
task_input_group,_= Group.objects.get_or_create(name='Task Input Worker')

vol_perms = []
con_perms = [] 
org_perms = [] 
eve_perms = [] 
prj_perms = []
tsk_perms = []

p_get = Permission.objects.get

#Add volunter permissions
vol_perms.append( p_get(codename='contact_view_related') )

vol_perms.append( p_get(codename='project_view_related') )
vol_perms.append( p_get(codename='project_assign_admin') )
vol_perms.append( p_get(codename='project_change_admin') )
vol_perms.append( p_get(codename='project_delete_admin') )
vol_perms.append( p_get(codename='project_down_sum_related') )

vol_perms.append( p_get(codename='task_view_related') )
vol_perms.append( p_get(codename='task_assign_admin') )
vol_perms.append( p_get(codename='task_add_admin') )
vol_perms.append( p_get(codename='task_change_admin') )
vol_perms.append( p_get(codename='task_delete_admin') )
vol_perms.append( p_get(codename='task_down_sum_related') )

#Add contact input permissions
con_perms.append( p_get(codename='add_contact') )
con_perms.append( p_get(codename='change_contact') )
con_perms.append( p_get(codename='contact_view_all') )
con_perms.append( p_get(codename='contact_view_events') )

#Add organization input permissions
org_perms.append( p_get(codename='add_organization') )
org_perms.append( p_get(codename='change_organization') )
org_perms.append( p_get(codename='organization_view_all') )

#Add event input permissions
eve_perms.append( p_get(codename='add_event') )
eve_perms.append( p_get(codename='change_event') )
eve_perms.append( p_get(codename='event_view_all') )
eve_perms.append( p_get(codename='contact_view_events') )

#Add project input permissions
prj_perms.append( p_get(codename='add_project') )
prj_perms.append( p_get(codename='change_project') )
prj_perms.append( p_get(codename='project_view_all') )
prj_perms.append( p_get(codename='project_assign') )
prj_perms.append( p_get(codename='contact_view_projects') )

#Add task input permissions
tsk_perms.append( p_get(codename='add_task') )
tsk_perms.append( p_get(codename='change_task') )
tsk_perms.append( p_get(codename='task_view_all') )
tsk_perms.append( p_get(codename='task_assign') )
tsk_perms.append( p_get(codename='contact_view_tasks') )

for perm in vol_perms:
	volunteer_group.permissions.add(perm)

for perm in con_perms:
	contact_input_group.permissions.add(perm)

for perm in org_perms:
	organization_input_group.permissions.add(perm)

for perm in eve_perms:
	event_input_group.permissions.add(perm)

for perm in prj_perms:
	project_input_group.permissions.add(perm)

for perm in tsk_perms:
	task_input_group.permissions.add(perm)

