from django.contrib import admin
from .models import Organization, Contact, ContactTypeTag
from .models import Project, ProjectContactAssoc
from .models import Task, TaskContactAssoc
from .models import Event

# Register your models here.
admin.site.register(Organization)
admin.site.register(Contact)
admin.site.register(ContactTypeTag)

admin.site.register(Project)
admin.site.register(ProjectContactAssoc)

admin.site.register(Task)
admin.site.register(TaskContactAssoc)

admin.site.register(Event)