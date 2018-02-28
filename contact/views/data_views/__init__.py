
from table import views

#Used by several different classes  
class PKFeedDataView(views.FeedDataView):
    """
    Some of our data feeds require a pk argument.
    But the get_queryset only accepts self as an argument!
    That's just fine - we'll save the primary key so we can use it later.
    """
    def get(self, request, *args, **kwargs):
        self.pk_arg = kwargs['pk']
        return super(PKFeedDataView, self).get(request, *args, **kwargs)

#Actual object views
from .data_list_views import *

#Views for project assocs - mostly assigning to projects
from .data_project_views import *

#Views for task assocs - mostly assigning to tasks
from .data_task_views import *

#Views for contact assocs - mostly viewing a contact's assocs
from .data_contact_views import *

#Views for dashboard assocs - for a user viewing their own assocs
from .data_dashboard_views import *