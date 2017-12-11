from django.contrib.auth.models import User
from django.urls import reverse 
from django.db import models

import datetime

class Organization(models.Model):
    """
    Model representing a contact
    """
    name = models.CharField(max_length=50, help_text="The name of this organization.")
    notes = models.TextField(max_length=1000, help_text="Any extra notes for this organization.", blank=True)

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

# Create your models here.
class Contact(models.Model):
    """
    Model representing a contact
    """
    name = models.CharField(max_length=50, help_text="The name of your contact.")

    email = models.EmailField(help_text="The contact's email address.", null=True, blank=True)

    phone = models.CharField(max_length=20, help_text="The phone number of your contact.", null=True, blank=True)

    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="contacts")

    notes = models.TextField(max_length=1000, help_text="Any extra notes for this contact.", blank=True)

    user_link = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

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
    def type_tags(self):
        return ContactTypeTag.objects.filter(contact__exact=self)

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
        ('_f', 'Corporate/Foundation'),
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
        ordering = ['contact', '-tag_type']

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
    title = models.CharField(max_length=50, help_text="Shorthand for referring to this project.")
    notes = models.TextField(max_length=1000, help_text="Any extra notes for this project.", blank=True)

    # ManyToManyField used because many contacts can be assigned to many projects.
    # associated = models.ManyToManyField(Contact, help_text="Who is associated with this project?")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.title

    @property
    def associated_contacts(self):
        return Contact.objects.filter(tasks__proj=self).distinct()
        #return self.task_set.contact_set

    @property
    def tasks(self):
        return self.task_set

    def get_absolute_url(self):
        """
        Returns the url to access a particular project.
        """
        return reverse('project-detail', args=[str(self.id)])

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
    complete = models.BooleanField(help_text="Is this task complete?")

    #Deadline for this task
    deadline = models.DateField(null=True, blank=True, help_text="What is the deadline for this task?")

    #notes for this task
    notes = models.TextField(max_length=555, help_text="Any extra notes for this project.", blank=True)

    class Meta: 
        unique_together = ( 'brief', 'proj',)
        ordering = ['deadline','complete',]


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

class TaskContactAssoc(models.Model):
    """
    Model representing an association with a task
    """
    #Possible Choices
    ASSOC_TYPE_LIST = (
        ('as', 'Assigned'),
        ('cr', 'Creator'),
        ('ta', 'Target'),
        ('na', 'Non-Specified Role')
    )

    #The contact for this task
    con  = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="task_assocs")
    
    #The task for this contact
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="con_assocs")

    #The associated type list
    tag_type = models.CharField(max_length=2, choices=ASSOC_TYPE_LIST, default='na')

    class Meta: 
        unique_together = ( 'con', 'task', )
        ordering = ['con', 'task', 'tag_type', ]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.task.brief[:25] + '(' + self.con.name[:25] + ')'
