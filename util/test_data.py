from django.contrib.auth.models import User, Group

import datetime
import random

import contact.models as models

#Delete all the existing objects
models.ContactTypeTag.objects.all().delete()
models.ProjectContactAssoc.objects.all().delete()
models.TaskContactAssoc.objects.all().delete()
models.Task.objects.all().delete()
models.Project.objects.all().delete()
models.Contact.objects.all().delete()
models.Event.objects.all().delete()
models.Organization.objects.all().delete()
User.objects.all().delete()

"""
MAKE CONTACTS
"""
contact_info = [
	("Clarence Cunningham", "clarkham@notmail.com", "666.222.4444"),
	("Hubert Thompson", "hueytom@notmail.com", "+34 (333) 000-1111"),
	("Randall Parrish", "randyonparr@notmail.com", "555 999 8888"),
	("Lynne Caldwell", "lycald@notmail.com", "111.222.3333"),
	("Jacqueline Washington", "jaqiwashi@notmail.com", "+0 777 321 0123"),
	("Claire Hull", "chull@notmail.com", "777 333 4444"),
	("Zachary Russell", "zachrussels@notmail.com", "555.222.3333"),
	("Floyd Fletcher", "ff@notmail.com", "867 5309"),
	("Parker Pickett", "misterpicket@notmail.com", "1-900-490-FREAK"),
	("Aubrey Peterson", "autopete@notmail.com", "666-777-4444"),
	("Evelyn Brooks", "ebrooks@notmail.com", "838-383-3838"),
	("Ella Thompson", "aguasmarcos@notmail.com", "222-6666"),
	("Lee Hanson", None, None),
	("Bobby House", None, None),
	("Percy Snider", None, None),
	("Sally Bryant", None, None),
	("Mindy McConnell", None, None),
	("Vanessa Hayes", None, None)
]

contact_list = []

for name, email, phone in contact_info:
	inst = models.Contact(
		name=name, email=email, phone=phone
	)
	inst.save()
	contact_list.append(inst)

"""
MAKE CONTACT TAGS
"""
tag_info = [
	['vo', 'pr'], ['vo', 'do'], ['pr'], ['do'], ['_f'], ['_g'],
]
random.shuffle(tag_info)

index = 0

for con in contact_list:
	tag_list = tag_info[index]

	for tag in tag_list:
		tag_inst = models.ContactTypeTag(contact=con, tag_type=tag)
		tag_inst.save()

	index = (index + 1)
	if index >= len(tag_info):
		index = 0
		random.shuffle(tag_info)

"""
MAKE ORGANIZATIONS
"""
grant_org = models.Organization(name="GoodGrants.com")
grant_org.save()
grant_list = models.Contact.objects.filter(tags__tag_type='_g')
for con in grant_list:
	con.org = grant_org
	con.save()

corporate_org = models.Organization(name="The Corporate Sphere")
corporate_org.save()
corporate_list = models.Contact.objects.filter(tags__tag_type='_f')
for con in corporate_list:
	con.org = corporate_org
	con.save()

"""
MAKE EVENTS
"""
event_names = [
	"The Waters of March", "The Sunday-day Spectacular", 
	"Friday Sculpture Workshop"
]

for name in event_names:
	inst = models.Event(name=name)
	inst.save()

	for con in random.sample( list( models.Contact.objects.all() ), 4):
		con.events.add(inst)
		con.save()

"""
MAKE USERS
"""
volunteer_list = models.Contact.objects.filter(tags__tag_type='vo')

admin = User.objects.create_user(
	username="admin", password="baseball123", 
	is_staff=True, is_superuser = True, is_active = True
)
admin.save()

vol_user = User.objects.create_user(
	username="volunteer", password="baseball123", 
	is_staff=True, is_superuser = False, is_active = True
)
vol_user.save()

input_user = User.objects.create_user(
	username="input", password="baseball123", 
	is_staff=True, is_superuser = False, is_active = True
)
input_user.save()

con = volunteer_list[0]
con.user_link = admin
con.save()

group = Group.objects.get(name='Volunteer')
group.user_set.add(vol_user)
con = volunteer_list[1]
con.user_link = vol_user
con.save()

group = Group.objects.get(name='Contact Input Worker')
group.user_set.add(input_user)
con = volunteer_list[2]
con.user_link = input_user
con.save()

"""
MAKE PROJECTS
"""
user_cons = models.Contact.objects.exclude(user_link=None)

project_info = [
	#All completed
	("Completed Fundraiser", datetime.date(year=2017, month=6, day=13), True, volunteer_list[0]),
	#Incomplete
	("Future Fundraiser", datetime.date.today() + datetime.timedelta(days=356 * 10), False, volunteer_list[0]),          
	#Overdue
	("A Very Off-Schedule Project", datetime.date(2017, 6, 5), False, volunteer_list[0]), 
	#No Deadline, Incomplete
	("A Project With an Irrelevant Timeline", None, False, volunteer_list[0])
]

project_list = []

for title, due_date, completed, user_con in project_info:
	project = models.Project(
		title=title, deadline=due_date, complete=completed
	)
	project.save()
	creator = models.ProjectContactAssoc(
		con=user_con, proj=project, tag_type='cr'
	)
	creator.save()

	project_list.append(project)

"""
ASSIGN CONTACTS TO PROJECTS
"""
old_p = None
#Step 1: Assign lead to projects
for _ in range(2):
	p = random.choice(project_list)
	while p == old_p:
		p = random.choice(project_list)
	old_p = p
	creator = models.ProjectContactAssoc(
		con=volunteer_list[1], proj=p, tag_type='le'
	)
	creator.save()

#Step 2: Assign resources to projects
for p in project_list:
	poss_con = list( models.Contact.objects.exclude(
		proj_assocs__tag_type__in=['as', 'le', 're', 'na'], proj_assocs__proj=p
	))
	for _ in range(3):
		random.shuffle(poss_con)
		con = poss_con.pop()

		resource = models.ProjectContactAssoc(
			con=con, proj=p, tag_type='re'
		)
		resource.save()


#Step 3: Assign volunteers to projects
for p in project_list:
	poss_con = list( models.Contact.objects.exclude(
		proj_assocs__tag_type__in=['as', 'le', 're', 'na'], proj_assocs__proj=p
	).filter(tags__tag_type='vo') )
	for _ in range(2):
		random.shuffle(poss_con)
		con = poss_con.pop()

		assigned = models.ProjectContactAssoc(
			con=con, proj=p, tag_type='as'
		)
		assigned.save()
"""
MAKE TASKS
"""
task_list = []
for i in range(15):
	name = "Task " + str(i + 1)

	if i % 3 == 0: #No deadline
		deadline = None
	elif i % 2 == 0: #Overdue deadline
		deadline = datetime.date.today() - datetime.timedelta(days=7)
	else: #Far future deadline
		deadline = datetime.date.today() + datetime.timedelta(days=7)

	if i < 10:
		p = random.choice(project_list)
	else:
		p = None

	complete = (random.randint(0, 1) == 0)
	inst = models.Task(brief=name, proj=p, complete=complete, deadline=deadline)
	inst.save()
	task_list.append(inst)

	creator = models.TaskContactAssoc(
		con=volunteer_list[0], task=inst, tag_type='cr'
	)
	creator.save()

"""
ASSIGN CONTACTS TO TASKS
"""
#Step 1: Add assignees
for t in task_list:
	con_list = None
	if t.proj:
		con_list = list(models.Contact.objects.filter(
			proj_assocs__proj=t.proj, proj_assocs__tag_type__in=['as','le']
		))
	else:
		con_list = list(models.Contact.objects.filter(tags__tag_type='vo'))
	for _ in range( min(2, len(con_list) ) ):
		random.shuffle(con_list)
		con = con_list.pop()
		assign = models.TaskContactAssoc(
			con=con, task=t, tag_type='as'
		)
		assign.save()

#Step 2: Add targets
for t in task_list:
	con_list = list(models.Contact.objects.exclude(
		task_assocs__task=t, task_assocs__tag_type__in=['as', 'ta', 're', 'na']
	))
	for _ in range( min(2, len(con_list) ) ):
		random.shuffle(con_list)
		con = con_list.pop()
		target = models.TaskContactAssoc(
			con=con, task=t, tag_type='ta'
		)
		target.save()

#Step 3: Add resources
for t in task_list:
	con_list = list(models.Contact.objects.exclude(
		task_assocs__task=t, task_assocs__tag_type__in=['as', 'ta', 're', 'na']
	))
	for _ in range( min(2, len(con_list) ) ):
		random.shuffle(con_list)
		con = con_list.pop()
		resource = models.TaskContactAssoc(
			con=con, task=t, tag_type='re'
		)
		resource.save()
