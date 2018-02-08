from django.contrib.auth.models import User
from django.urls import reverse 
from django.db import models

import django_bleach

import datetime
import bleach
import math

class Organization(models.Model):
    """
    Model representing an organization that a contact belongs to
    """
    name = models.CharField(max_length=50, help_text="The name of this organization.")
    notes = models.TextField(max_length=2500, help_text="Any extra notes for this organization.", blank=True)

    class Meta:
        permissions = (
            ("organization_view_all", "View all organizations."),
            ("organization_down_sum_all", "Download organizations summaries."),
        )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular project.
        """
        return reverse('organization-detail', args=[str(self.id)])

    @property
    def notes_bleach_trim(self):
        char_lim = 97
        ret_val = None

        if self.notes:
            ret_val = bleach.clean( self.notes, strip=True, tags=[''])
            
            if len(ret_val) > char_lim:
                ret_val = ret_val[:char_lim] + '...'

        return ret_val

    @property
    def contact_count(self):
        return self.contacts.count()

class Event(models.Model):
    """
    Model representing an event / workshop.
    Essentially, a piece of data describing what events / workshops a contact
    has attended.
    """
    name = models.CharField(max_length=50, help_text="The name of this event / workshop.")
    notes = models.TextField(max_length=2500, help_text="Any extra notes for this event / workshop.", blank=True)

    class Meta:
        permissions = (
            ("event_view_all", "View all events / workshops."),
            ("event_down_sum_all", "Download events / workshops summaries."),
        )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular project.
        """
        return reverse('event-detail', args=[str(self.id)])

    @property
    def notes_bleach_trim(self):
        char_lim = 97
        ret_val = None

        if self.notes:
            ret_val = bleach.clean( self.notes, strip=True, tags=[''])
            
            if len(ret_val) > char_lim:
                ret_val = ret_val[:char_lim] + '...'

        return ret_val

    @property
    def contact_count(self):
        return self.contacts.count()

# Create your models here.
class Contact(models.Model):
    """
    Model representing a contact
    """
    name = models.CharField(max_length=50, help_text="The name of your contact.")
    email = models.EmailField(help_text="The contact's email address.", null=True, blank=True)
    phone = models.CharField(max_length=20, help_text="The phone number of your contact.", null=True, blank=True)

    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="contacts")
    events = models.ManyToManyField(Event, related_name="contacts")

    notes = models.TextField(max_length=2500, help_text="Any extra notes for this contact.", blank=True)
    user_link = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (
            ("contact_view_all", "View all contacts."),
            ("contact_view_related", "View related contacts."),

            ("contact_view_projects", "View contact's projects."),
            ("contact_view_tasks", "View contact's tasks."),
            ("contact_view_events", "View contact's events."),

            ("contact_down_sum_all", "Download overall contact summary."),
            ("contact_down_sum_each", "Download individual contact summaries."),
        )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular project.
        """
        return reverse('contact-detail', args=[str(self.id)])

    @property
    def notes_bleach_trim(self):
        char_lim = 97
        ret_val = None

        if self.notes:
            ret_val = bleach.clean( self.notes, strip=True, tags=[''])
            
            if len(ret_val) > char_lim:
                ret_val = ret_val[:char_lim] + '...'

        return ret_val


    # #########
    # Type Tags
    # #########
    @property
    def type_tags(self):
        return ContactTypeTag.objects.filter(contact__exact=self)

    @property
    def type_list_string(self):
        out = ""
        for tag in self.type_tags.all():
            out += tag.get_tag_type_display() + " "
        return out

    @property
    def is_volunteer(self):
        return self.type_tags.filter(tag_type__exact="vo").exists()

    @property
    def is_prospect(self):
        return self.type_tags.filter(tag_type__exact="pr").exists()

    @property
    def is_donor(self):
        return self.type_tags.filter(tag_type__exact="do").exists()

    @property
    def is_resource(self):
        return self.type_tags.filter(tag_type__exact="_g").exists()

    @property
    def is_foundation(self):
        return self.type_tags.filter(tag_type__exact="_f").exists()

    # ##################
    # Tasks and Projects
    # ##################
    @property
    def associated_projects(self):
        return Project.objects.filter(tasks__contacts=self).distinct()

    @property
    def assigned_tasks(self):
        return self.get_tasks('as')

    @property
    def targeted_by_tasks(self):
        return self.get_tasks('ta')

    @property
    def nonaligned_tasks(self):
        return self.get_tasks('na')

    @property
    def created_tasks(self):
        return self.get_tasks('cr')       

    def get_tasks(self, tag=None):
        if tag is None:
            return self.task_set
        else:
            return Task.objects.filter(taskcontactassoc__con=self, taskcontactassoc__tag_type__exact=tag)

class ContactTypeTag(models.Model):
    
    CONTACT_TYPE_LIST = (
        ('do', 'Donor'),
        ('pr', 'Prospect'),
        ('vo', 'Volunteer'),
        ('_f', 'Corporate / Foundation'),
        ('_g', 'Grant Resource'),
    )

    CONTACT_ABBRV = {
        'do' : "D",
        'pr' : "P",
        'vo' : "V", 
        '_f' : "CF",
        '_g' : "GR",
    }

    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name="tags")

    tag_type = models.CharField(max_length=2, choices=CONTACT_TYPE_LIST, default='pr')

    class Meta: 
        unique_together = ( 'contact', 'tag_type',)

    def get_contact_abbrv(self):
        """
        Returns a css class, dependent on the contact type
        """
        return self.CONTACT_ABBRV[self.tag_type]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.contact.name + ' (' + self.get_tag_type_display() + ')'

class Project(models.Model):
    """
    Model representing a project
    """
    title = models.CharField(
        max_length=50, help_text="Shorthand for referring to this project.",
        unique=True
    )

    notes = models.TextField(
        max_length=2500, help_text="Any extra notes for this project.", 
        blank=True
    )

    #Deadline for this task
    deadline = models.DateField(
        null=True, blank=True, help_text="What is the deadline for this project?"
    )

    #Is this task complete?
    complete = models.BooleanField(help_text="Is this project complete?", default=False)

    #Who is this project associated with?
    contacts = models.ManyToManyField(
        Contact, through='ProjectContactAssoc', 
        help_text="Who is associated with this project?", 
        related_name="projects"
    )

    class Meta: 
        ordering = ['deadline','complete',]
        permissions = (
            ("project_view_all", "View all projects."),
            ("project_view_related", "View related projects."),

            ("project_assign", "Assign contacts to projects"),
            ("project_assign_admin", "Assign contacts to admined projects"),

            ("project_change_admin", "Change admined project tasks"),
            ("project_delete_admin", "Delete admined project tasks"),

            ("project_down_sum_all", "Download overall project summary."),
            ("project_down_sum_each", "Download individual project summaries."),
            ("project_down_sum_related", "Download related project summaries."),
        )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular project.
        """
        return reverse('project-detail', args=[str(self.id)])

    @property
    def complete_percent(self):
        val = 0

        if self.tasks.exists():
            val = self.tasks.filter(complete__exact=True).count() / self.tasks.count()
            val *= 100
            val = math.floor(val)

        return val 

    def percentage_formatted(self):
        return str(self.complete_percent) + '%'

    @property
    def notes_bleach_trim(self):
        char_lim = 247
        ret_val = None

        if self.notes:
            ret_val = bleach.clean( self.notes, strip=True, tags=[''])
            
            if len(ret_val) > char_lim:
                ret_val = ret_val[:char_lim] + '...'

        return ret_val

    @property
    def status(self):
        if self.complete:
            return "Completed"
        elif (self.deadline is None) or (datetime.date.today() < self.deadline):
            return "Incomplete"
        else:
            return "Overdue"

class Task(models.Model):
    """
    Model representing a task that needs doing
    """
    #A brief description for quickly referring to this task
    brief = models.CharField(max_length=75, help_text="A brief description for quickly referring to this task. 75 character max.")

    #The associated project, if any
    proj = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    #Who is this task is associated with?
    contacts = models.ManyToManyField(Contact, through='TaskContactAssoc', help_text="Who is associated with this task?", related_name="tasks")

    #Is this task complete?
    complete = models.BooleanField(help_text="Is this task complete?", default=False)

    #Deadline for this task
    deadline = models.DateField(null=True, blank=True, help_text="What is the deadline for this task?")

    #notes for this task
    notes = models.TextField(max_length=2500, help_text="Any extra notes for this project.", blank=True)

    class Meta: 
        unique_together = ( 'brief', 'proj',)
        ordering = ['deadline','complete',]
        permissions = (
            ("task_view_all", "View all tasks."),
            ("task_view_related", "View related tasks."),

            ("task_assign", "Assign contacts to tasks"),
            ("task_assign_admin", "Assign contacts to admined tasks"),

            ("task_add_to", "Add tasks to any project"),
            ("task_add_admin", "Add tasks to admined projects"),
            ("task_change_admin", "Change admined project tasks"),
            ("task_delete_admin", "Delete admined project tasks"),

            ("task_down_sum_all", "Download overall task summary."),
            ("task_down_sum_each", "Download individual task summaries."),
            ("task_down_sum_related", "Download related task summaries."),
        )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.brief

    def get_absolute_url(self):
        """
        Returns the url to access a particular task.
        """
        return reverse('task-detail', args=[str(self.id)])

    @property
    def notes_bleach_trim(self):
        char_lim = 97
        ret_val = None

        if self.notes:
            ret_val = bleach.clean( self.notes, strip=True, tags=[''])
            
            if len(ret_val) > char_lim:
                ret_val = ret_val[:char_lim] + '...'

        return ret_val


    @property
    def assigned_contacts(self):
        return self.get_contacts('as')

    @property
    def targeted_contacts(self):
        return self.get_contacts('ta')

    @property
    def nonaligned_contacts(self):
        return self.get_contacts('na')

    @property
    def creator_contacts(self):
        return self.get_contacts('cr')        

    def get_contacts(self, tag=None):
        if tag is None:
            return self.contacts.all()
        else:
            return self.contacts.filter(task_assocs__tag_type__exact=tag) 

    @property
    def overdue(self):
        if self.deadline is None:
            return False

        return datetime.date.today() > self.deadline 

    @property
    def status(self):
        if self.complete:
            return "Completed"
        elif (self.deadline is None) or (datetime.date.today() < self.deadline):
            return "Incomplete"
        else:
            return "Overdue"

class TaskContactAssoc(models.Model):
    """
    Model representing an association with a task
    """
    #Possible Choices
    ASSOC_TYPE_LIST = (
        ('as', 'Assigned'),
        ('cr', 'Creator'),
        ('ta', 'Target'),
        ('re', 'Resource'),
        ('na', 'Unspecified')
    )

    #The contact for this task
    con  = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="task_assocs")
    
    #The task for this contact
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="con_assocs")

    #The associated type list
    tag_type = models.CharField(max_length=2, choices=ASSOC_TYPE_LIST, default='na')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.task.brief[:25] + '(' + self.con.name[:25] + ')'

    def save(self, *args, **kwargs):
        #If we're making a creator tag...
        if self.tag_type == 'cr':
            #THERE CAN ONLY BE ONE CREATOR!
            other = TaskContactAssoc.objects.filter(tag_type='cr', task=self.task)
            if( other.exists() ):
                message = "Task '{0}' cannot have two creators!"
                raise Exception(message.format(self.task.brief))
        else:
            other = TaskContactAssoc.objects.filter(tag_type__in=['as','ta','re','na'], task=self.task, con=self.con)
            if( other.exists() ):
                message = "A non-creator relationship already exists between task '{0}' and '{1}'!"
                raise Exception( message.format(self.task.brief, self.con.name) )
        super(TaskContactAssoc, self).save(*args, **kwargs)
    
            

class ProjectContactAssoc(models.Model):
    """
    Model representing an association with a task
    """
    #Possible Choices
    ASSOC_TYPE_LIST = (
        ('as', 'Assigned'),
        ('le', 'Project Lead'),
        ('cr', 'Creator'),
        ('re', 'Resource'),
        ('na', 'Unspecified')
    )

    #The contact for this task
    con  = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="proj_assocs")
    
    #The task for this contact
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="con_assocs")

    #The associated type list
    tag_type = models.CharField(max_length=2, choices=ASSOC_TYPE_LIST, default='na')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.proj.title[:25] + '(' + self.con.name[:25] + ')'

    def save(self, *args, **kwargs):
        #If we're making a creator tag...
        if self.tag_type == 'cr':
            #THERE CAN ONLY BE ONE CREATOR!
            other = ProjectContactAssoc.objects.filter(tag_type='cr', proj=self.proj)
            if( other.exists() ):
                message = "Project '{0}' cannot have two creators!"
                raise Exception( message.format(self.proj.title) )
        else:
            other = ProjectContactAssoc.objects.filter(tag_type__in=['as','ta','re','na'], proj=self.proj, con=self.con)
            if( other.exists() ):
                message = "A non-creator relationship already exists between project '{0}' and '{1}'!"
                raise Exception( message.format(self.proj.title, self.con.name) )
        super(ProjectContactAssoc, self).save(*args, **kwargs)
