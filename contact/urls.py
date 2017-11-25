from django.conf.urls import url

from . import views


urlpatterns = [
	#reroute non-specific requests to the index
    url(r'^$', views.index, name='index'),

    url(r'^dashboard/$', views.my_dashboard, name='my-dashboard'),

    url(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),
    url(r'^contact/(?P<pk>\d+)$', views.ContactDetailView.as_view(), name='contact-detail'),

    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),

    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name='task-detail'),

    url(r'^tasks/mine/$', views.MyTaskView.as_view(), name='my-assocs'),
]

