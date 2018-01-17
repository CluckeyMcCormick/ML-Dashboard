from contact import models

#Get (a semi-random / the first available) task with a creator
task = models.Task.objects.filter(con_assocs__tag_type='cr').first()
#Get (a semi-random / the first available) contact
contact = models.Contact.objects.get_queryset().first()
#TEST - TWO CREATOR CONTACTS FOR TASK
try:
	thing = models.TaskContactAssoc.objects.create(task=task, con=contact, tag_type='cr')
	thing.save()
	thing.delete()
except Exception as e:
	print(e)

#Get (a semi-random / the first available) task with a non-creator relationship
task = models.Task.objects.filter(con_assocs__tag_type__in=['as', 'ta', 're', 'na']).first()
#Get (a semi-random / the first available) contact 
#with a relationship to that task
contact = models.TaskContactAssoc.objects
contact = contact.filter(task=task, tag_type__in=['as', 'ta', 're', 'na'])
contact = contact.first().con
#TEST - EXTRA NONCREATOR RELATION (TASK)
try:
	thing = models.TaskContactAssoc.objects.create(task=task, con=contact, tag_type='as')
	thing.save()
	thing.delete()
except Exception as e:
	print(e)

#Get (a semi-random / the first available) project with a creator
project = models.Project.objects.filter(con_assocs__tag_type='cr').first()
#Get (a semi-random / the first available) contact
contact = models.Contact.objects.get_queryset().first()
#TEST - TWO CREATOR CONTACTS FOR PROJECT
try:
	thing = models.ProjectContactAssoc.objects.create(proj=project, con=contact, tag_type='cr')
	thing.save()
	thing.delete()
except Exception as e:
	print(e)

#Get (a semi-random / the first available) project with a non-creator relationship
project = models.Project.objects
project = project.filter(con_assocs__tag_type__in=['as', 'ta', 're', 'na']).first()
#Get (a semi-random / the first available) contact 
#with a relationship to that task
contact = models.ProjectContactAssoc.objects
contact = contact.filter(proj=project, tag_type__in=['as', 'le', 're', 'na'])
contact = contact.first().con
#TEST - EXTRA NONCREATOR RELATION (PROJECT)
try:
	thing = models.ProjectContactAssoc.objects.create(proj=project, con=contact, tag_type='as')
	thing.save()
	thing.delete()
except Exception as e:
	print(e)