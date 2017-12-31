from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from django.db.utils import OperationalError

from django import forms

from .models import (
    ContactTypeTag, Task, TaskContactAssoc,
    Organization, Contact, Project,
)

class ContactForm(forms.ModelForm):

    con_type = forms.MultipleChoiceField(
        choices= ContactTypeTag.CONTACT_TYPE_LIST, 
        widget= forms.CheckboxSelectMultiple,
        label= ugettext_lazy('Contact Type'),
        help_text= ugettext_lazy('Select all the labels that apply to this contact.'),
        required=False
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'org', 'notes']
        widgets = {
            'notes': forms.Textarea( attrs={'max_length' : 1000} ),
        }
        labels = {
            'org': ugettext_lazy('Organization'),
        }
        help_texts = {
            'org': ugettext_lazy('This contact\'s associated organization.'),
        }

    def handle_contact_tags(self, contact):
        #First, get all the tags for this contact
        tags = ContactTypeTag.objects.filter(contact__exact=contact.pk)

        #Secondly, we grab our tag choices
        chosen_tags = self.cleaned_data['con_type']

        #Third, we delete all the tags that weren't selected, but exist
        for delete_target in tags.exclude(tag_type__in=chosen_tags):
            delete_target.delete()

        #Fourth, we create all the targets that don't exist
        for tag_val in chosen_tags:
            #If the tag value doesn't exist
            if not tags.filter(tag_type__exact=tag_val).exists():
                #Create it!
                new_tag = ContactTypeTag(contact=contact, tag_type=tag_val)
                new_tag.save()

class OrgForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = '__all__'

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'notes', 'deadline']
        widgets = {
            'notes': forms.Textarea( attrs={'max_length' : 1000} ),
            'deadline': forms.SelectDateWidget(),
        }

class TaskForm(forms.ModelForm):

    try:
        volunteer_query = Contact.objects.filter(tags__tag_type__exact='vo')
        volunteer_query = volunteer_query.values_list('id', 'name')
        volunteer_query = volunteer_query.order_by('name')

        target_query = Contact.objects.filter(tags__tag_type__exact='pr')
        target_query = target_query.exclude(tags__tag_type__in=['cr', 'vo'])
        target_query = target_query.values_list('id', 'name')
        target_query = target_query.order_by('name')

        volunteer_choices = [(pk_id, name) for pk_id, name in volunteer_query]
        target_choices = [(pk_id, name) for pk_id, name in target_query]
    except OperationalError:
        volunteer_choices = [(None, "------")]
        target_choices = [(None, "------")]

    volunteers = forms.MultipleChoiceField(
        volunteer_choices, 
        widget= forms.CheckboxSelectMultiple,
        label= ugettext_lazy('Assigned Volunteers'),
        help_text= ugettext_lazy('Choose volunteers to be assigned to this task.'),
        required=False,
        #empty_label= None
    )

    targets = forms.MultipleChoiceField(
        target_choices, 
        widget= forms.CheckboxSelectMultiple,
        label= ugettext_lazy('Assigned Volunteers'),
        help_text= ugettext_lazy('Choose people that will need to be contacted for this task.'),
        required=False,
        #empty_label= None
    )

    class Meta:
        model = Task
        fields = ['brief', 'complete', 'deadline', 'proj', 'notes']
        labels = {
            'complete': ugettext_lazy('Complete?'),
            'brief' : ugettext_lazy('Brief Description / Title'),
            'proj'  : ugettext_lazy('Project'),
        }

        help_texts = {
            'proj' : ugettext_lazy('The project this task is associated with.'),
        }

        widgets = {
            'deadline': forms.SelectDateWidget(),
            'proj': forms.Select(attrs={'disabled': True}),
        }

    def handle_task_assignments(self, task):
        #First, get all the task_assocs for this contact

        tasks_assocs = TaskContactAssoc.objects.filter(task__exact=task.pk)

        #Secondly, we grab our contact choices
        volunteer_list = self.cleaned_data['volunteers']
        target_list = self.cleaned_data['targets']

        volunteer_query = Contact.objects.filter(id__in=volunteer_list)
        target_query = Contact.objects.filter(id__in=target_list)

        delete_list = tasks_assocs.exclude(con__in=volunteer_list + target_list)
        delete_list = delete_list.exclude(tag_type__exact='cr')

        #Third, we delete all the tags that weren't selected, but exist
        for delete_target in delete_list:
            delete_target.delete()

        #Fourth, we create all the targets that don't exist
        for vol_con in volunteer_query:
            #If we don't have an association for the listed contact
            if not tasks_assocs.filter(con__exact=vol_con).exists():
                #Create one!
                new_assoc = TaskContactAssoc(con=vol_con, task=task, tag_type='as')
                new_assoc.save()

        #Fifth, we create all the targets that don't exist
        for targ_con in target_query:
            #If we don't have an association for the listed contact
            if not tasks_assocs.filter(con__exact=targ_con).exists():
                #Create one!
                new_assoc = TaskContactAssoc(con=targ_con, task=task, tag_type='ta')
                new_assoc.save()                            
            
class MyTaskSearchForm(forms.Form):
    brief_name = forms.CharField(min_length=0, max_length=75, strip=True)
    brief_name.label = 'Brief'
    brief_name.required = False

    #Possible Choices
    ASSOC_ROLE_LIST = (
        ('no', ''),
        ('as', 'Assigned'),
        ('cr', 'Creator'),
        ('na', 'Non-Specified Role')
    )
    assoc_role = forms.ChoiceField(choices=ASSOC_ROLE_LIST)
    assoc_role.label = 'Role'
    assoc_role.required = False

    #Possible Choices
    COMPLETE_STATUS_LIST = (
        ('no', ''),
        ('un', 'All Unfinished'),
        ('in', 'Incomplete'),
        ('ov', 'Overdue'),
        ('co', 'Complete'),
    )
    task_stat = forms.ChoiceField(choices=COMPLETE_STATUS_LIST)
    task_stat.label = 'Complete?'
    task_stat.required = False

    """
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #Check date is not in past. 
        if data < datetime.date.today():
            raise ValidationError( ugettext_lazy('Invalid date - renewal in past') )

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError( ugettext_lazy('Invalid date - renewal more than 4 weeks ahead') )

        # Remember to always return the cleaned data.
        return data
    """