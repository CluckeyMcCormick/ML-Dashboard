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

    class Meta:
        model = Task
        fields = ['brief', 'deadline', 'proj', 'notes']
        labels = {
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