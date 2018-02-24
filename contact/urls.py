from django.conf.urls import url, include

from . import views

urlpatterns = [
	#reroute non-specific requests to the index
    #url(r'^$', views.index, name='index'),

    url(r'^$', views.my_dashboard),
    url(r'^dashboard/$', views.my_dashboard, name='my-dashboard'),
    url(r'^dashboard/print/$', views.my_dashboard_print, name='my-dashboard-print'),

    #
    # CONTACTS
    #
    url(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),
    url(r'^contacts/download/$', views.download_contact_dataset, name='contacts-all-download'),
    url(r'^contacts/download_volunteer/$', views.download_contact_volunteer_dataset, name='contacts-volunteer-download'),
    url(r'^contacts/download_prospect/$', views.download_contact_prospect_dataset, name='contacts-prospect-download'),
    url(r'^contacts/download_donor/$', views.download_contact_donor_dataset, name='contacts-donor-download'),
    url(r'^contacts/download_grant/$', views.download_contact_grant_dataset, name='contacts-grant-download'),
    url(r'^contacts/download_corporation/$', views.download_contact_corporation_dataset, name='contacts-corporation-download'),

    url(r'^contact/create/$', views.ContactCreate.as_view(), name='contact-create'),

    url(r'^contact/(?P<pk>\d+)$', views.ContactDetailView.as_view(), name='contact-detail'),
    url(r'^contact/(?P<pk>\d+)/print/$', views.ContactPrintView.as_view(), name='contact-print'),
    url(r'^contact/(?P<pk>\d+)/update/$', views.ContactUpdate.as_view(), name='contact-update'),
    url(r'^contact/(?P<pk>\d+)/delete/$', views.ContactDelete.as_view(), name='contact-delete'),

    #
    # ORGANIZATIONS
    #
    url(r'^orgs/$', views.OrgListView.as_view(), name='orgs'),
    url(r'^org/create/$', views.OrgCreate.as_view(), name='org-create'),

    url(r'^org/(?P<pk>\d+)$', views.OrgDetailView.as_view(), name='org-detail'),
    url(r'^org/(?P<pk>\d+)/print/$', views.OrgPrintView.as_view(), name='org-print'),
    url(r'^org/(?P<pk>\d+)/update/$', views.OrgUpdate.as_view(), name='org-update'),
    url(r'^org/(?P<pk>\d+)/delete/$', views.OrgDelete.as_view(), name='org-delete'),

    #
    # EVENTS
    #
    url(r'^events/$', views.EventListView.as_view(), name='events'),
    url(r'^events/create/$', views.EventCreate.as_view(), name='event-create'),

    url(r'^event/(?P<pk>\d+)$', views.EventDetailView.as_view(), name='event-detail'),
    url(r'^event/(?P<pk>\d+)/print/$', views.EventPrintView.as_view(), name='event-print'),
    url(r'^event/(?P<pk>\d+)/update/$', views.EventUpdate.as_view(), name='event-update'),
    url(r'^event/(?P<pk>\d+)/delete/$', views.EventDelete.as_view(), name='event-delete'),

    #
    # PROJECTS
    #
    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^projects/download/$', views.download_project_dataset, name='projects-all-download'),
    url(r'^projects/download_incomplete/$', views.download_project_incomplete_dataset, name='projects-incomplete-download'),

    url(r'^project/create/$', views.ProjectCreate.as_view(), name='project-create'),

    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^project/(?P<pk>\d+)/print/$', views.ProjectPrintView.as_view(), name='project-print'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'^project/(?P<pk>\d+)/delete/$', views.ProjectDelete.as_view(), name='project-delete'),

    url(r'^project/(?P<pk>\d+)/add_lead/$', views.ProjectAssoc_LeadView.as_view(), name='project-add-lead'),
    url(r'^project/(?P<pk>\d+)/add_volunteer/$', views.ProjectAssoc_AssignView.as_view(), name='project-add-volunteer'),
    url(r'^project/(?P<pk>\d+)/add_resource/$', views.ProjectAssoc_ResourceView.as_view(), name='project-add-resource'),

    url(r'^projects/mine/$', views.MyProjectView.as_view(), name='my-proj-assocs'),

    #
    # TASKS
    #
    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^tasks/download/$', views.download_task_dataset, name='tasks-all-download'),
    url(r'^tasks/download_incomplete/$', views.download_task_incomplete_dataset, name='tasks-incomplete-download'),

    url(r'^task/create/$', views.TaskCreate.as_view(), name='task-create'),

    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name='task-detail'),
    url(r'^task/(?P<pk>\d+)/print/$', views.TaskPrintView.as_view(), name='task-print'),
    url(r'^task/(?P<pk>\d+)/update/$', views.TaskUpdate.as_view(), name='task-update'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.TaskDelete.as_view(), name='task-delete'),

    url(r'^task/(?P<pk>\d+)/add_target/$', views.TaskAssocTargetView.as_view(), name='task-add-target'),
    url(r'^task/(?P<pk>\d+)/add_volunteer/$', views.TaskAssocAssignView.as_view(), name='task-add-volunteer'),
    url(r'^task/(?P<pk>\d+)/add_resource/$', views.TaskAssocResourceView.as_view(), name='task-add-resource'),

    #View for specifically creating bounded or un-bounded tasks
    url(r'^task/create/free_type/$', views.TaskUnboundCreate.as_view(), name='task-unbound-create'),
    url(r'^task/create/project_type/(?P<pk>\d+)/$', views.TaskProjectCreate.as_view(), name='task-project-create'),

    #View your associations with tasks - ergo, a derivative of tasks
    url(r'^tasks/mine/$', views.MyTaskView.as_view(), name='my-task-assocs'),

    #
    # USERS
    #
    url(r'^users/$', views.UserListView.as_view(), name='view-users'),
    url(r'^user/create/$', views.UserCreateView.as_view(), name='create-user'),

    #
    # DATA
    #
    url(r'^table/data/contact/$', views.ContactDataView.as_view(), name='table-data-contact'),
    url(r'^table/data/organization/$', views.OrganizationDataView.as_view(), name='table-data-organization'),
    url(r'^table/data/event/$', views.EventDataView.as_view(), name='table-data-event'),
    url(r'^table/data/project/$', views.ProjectDataView.as_view(), name='table-data-project'),
    url(r'^table/data/task/$', views.TaskDataView.as_view(), name='table-data-task'),

    url(r'^table/data/assign/lead/(?P<pk>\d+)$', views.AddLeadDataView.as_view(), name='table-data-assign-lead'),   
]


