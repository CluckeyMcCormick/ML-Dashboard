from django.contrib.auth.models import User
from django.urls import reverse 
from django.db import models

import datetime
import math

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
    title = models.CharField(
        max_length=50, help_text="Shorthand for referring to this project."
    )
    notes = models.TextField(
        max_length=1000, help_text="Any extra notes for this project.", 
        blank=True
    )

    #Deadline for this task
    deadline = models.DateField(
        null=True, blank=True, help_text="What is the deadline for this project?"
    )

    #Who is this project associated with?
    contacts = models.ManyToManyField(
        Contact, through='ProjectContactAssoc', 
        help_text="Who is associated with this project?", 
        related_name="projects"
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
    def notes_trimmed(self):
        char_lim = 247
        ret_val = None

        if self.notes:
            if len(self.notes) > char_lim:
                ret_val = self.notes[:char_lim] + '...'
            else:
                ret_val = self.notes

        return ret_val

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
        ('na', 'Unspecified')
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

class ProjectContactAssoc(models.Model):
    """
    Model representing an association with a task
    """
    #Possible Choices
    ASSOC_TYPE_LIST = (
        ('as', 'Assigned'),
        ('cr', 'Creator'),
        ('na', 'Unspecified')
    )

    #The contact for this task
    con  = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="proj_assocs")
    
    #The task for this contact
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="con_assocs")

    #The associated type list
    tag_type = models.CharField(max_length=2, choices=ASSOC_TYPE_LIST, default='na')

    class Meta: 
        unique_together = ( 'con', 'proj', )
        ordering = ['con', 'proj', 'tag_type', ]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.proj.title[:25] + '(' + self.con.name[:25] + ')'
