from django.conf.urls import url, include

from . import views


urlpatterns = [
	#reroute non-specific requests to the index
    #url(r'^$', views.index, name='index'),

    url(r'^$', views.my_dashboard),
    url(r'^dashboard/$', views.my_dashboard, name='my-dashboard'),

    #
    # CONTACTS
    #
    url(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),
    url(r'^contact/(?P<pk>\d+)$', views.ContactDetailView.as_view(), name='contact-detail'),
    url(r'^contact/create/$', views.ContactCreate.as_view(), name='contact-create'),
    url(r'^contact/(?P<pk>\d+)/update/$', views.ContactUpdate.as_view(), name='contact-update'),
    url(r'^contact/(?P<pk>\d+)/delete/$', views.ContactDelete.as_view(), name='contact-delete'),

    #
    # ORGANIZATIONS
    #
    url(r'^orgs/$', views.OrgListView.as_view(), name='orgs'),
    url(r'^org/(?P<pk>\d+)$', views.OrgDetailView.as_view(), name='org-detail'),
    url(r'^org/create/$', views.OrgCreate.as_view(), name='org-create'),
    url(r'^org/(?P<pk>\d+)/update/$', views.OrgUpdate.as_view(), name='org-update'),
    url(r'^org/(?P<pk>\d+)/delete/$', views.OrgDelete.as_view(), name='org-delete'),

    #
    # PROJECTS
    #
    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^project/create/$', views.ProjectCreate.as_view(), name='project-create'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'^project/(?P<pk>\d+)/delete/$', views.ProjectDelete.as_view(), name='project-delete'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'^project/assign/$', views.AssignContactView.as_view(), name='project-assign'),

    #
    # TASKS
    #
    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name='task-detail'),
    url(r'^task/create/$', views.TaskCreate.as_view(), name='task-create'),
    url(r'^task/(?P<pk>\d+)/update/$', views.TaskUpdate.as_view(), name='task-update'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.TaskDelete.as_view(), name='task-delete'),

    #View for specifically creating bounded or un-bounded tasks
    url(r'^task/create/free_type/$', views.TaskUnboundCreate.as_view(), name='task-unbound-create'),
    url(r'^task/create/project_type/(?P<pk>\d+)/$', views.TaskProjectCreate.as_view(), name='task-project-create'),

    #View your associations with tasks - ergo, a derivative of tasks
    url(r'^tasks/mine/$', views.MyTaskView.as_view(), name='my-assocs'),
]