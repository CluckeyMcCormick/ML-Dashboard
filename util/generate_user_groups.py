from django.contrib.auth.models import Group, Permission

volunteer_group,_ = Group.objects.get_or_create(name='Volunteer')
data_admin_group,_= Group.objects.get_or_create(name='Data Admin')

vol_perms = [] 
da_perms = []

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

#Add data admin permissions
da_perms.append( p_get(codename='add_organization') )
da_perms.append( p_get(codename='change_organization') )
da_perms.append( p_get(codename='delete_organization') )
da_perms.append( p_get(codename='organization_view_all') )
da_perms.append( p_get(codename='organization_down_sum_all') )

da_perms.append( p_get(codename='add_contact') )
da_perms.append( p_get(codename='change_contact') )
da_perms.append( p_get(codename='delete_contact') )
da_perms.append( p_get(codename='contact_view_all') )
da_perms.append( p_get(codename='contact_view_projects') )
da_perms.append( p_get(codename='contact_view_tasks') )
da_perms.append( p_get(codename='contact_down_sum_all') )
da_perms.append( p_get(codename='contact_down_sum_each') )

da_perms.append( p_get(codename='add_project') )
da_perms.append( p_get(codename='change_project') )
da_perms.append( p_get(codename='delete_project') )
da_perms.append( p_get(codename='project_view_all') )
da_perms.append( p_get(codename='project_assign') )
da_perms.append( p_get(codename='project_down_sum_all') )
da_perms.append( p_get(codename='project_down_sum_each') )

da_perms.append( p_get(codename='add_task') )
da_perms.append( p_get(codename='change_task') )
da_perms.append( p_get(codename='delete_task') )
da_perms.append( p_get(codename='task_view_all') )
da_perms.append( p_get(codename='task_assign') )
da_perms.append( p_get(codename='task_add_to') )
da_perms.append( p_get(codename='task_down_sum_all') )
da_perms.append( p_get(codename='task_down_sum_each') )

for perm in vol_perms:
	volunteer_group.permissions.add(perm)
	data_admin_group.permissions.add(perm)

for perm in da_perms:
	data_admin_group.permissions.add(perm)	