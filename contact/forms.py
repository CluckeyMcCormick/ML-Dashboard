from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db.utils import OperationalError
from django.utils.translation import ugettext_lazy

from django import forms

import django_select2.forms as select2
import tinymce

from .models import (
    ContactTypeTag, Task, TaskContactAssoc,
    Organization, Contact, Project, Event,
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
        fields = ['name', 'email', 'phone', 'org', 'events', 'notes']
        widgets = {
            'notes' : tinymce.TinyMCE(attrs={'cols': 60, 'rows': 15}),
            'events': select2.ModelSelect2MultipleWidget(model=Event, search_fields=['name__icontains']),
            'org' : select2.ModelSelect2Widget(
                model=Organization,
                search_fields=['name__icontains'],
            ),
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
        widgets = {
            'notes': tinymce.TinyMCE(attrs={'cols': 60, 'rows': 15}),
        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'notes']
        widgets = {
            'notes': tinymce.TinyMCE(attrs={'cols': 60, 'rows': 15}),
        }

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'notes', 'deadline']
        widgets = {
            'notes': tinymce.TinyMCE(attrs={'cols': 60, 'rows': 15}),
            'deadline': forms.SelectDateWidget(years=[str(v) for v in range(2017, 2035)]),
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
            'deadline': forms.SelectDateWidget(years=[str(v) for v in range(2017, 2035)]),
            'notes': tinymce.TinyMCE(attrs={'cols': 60, 'rows': 15}),
            'proj' : select2.ModelSelect2Widget(
                model=Project,
                search_fields=['title__icontains'],
            ),
        }                          

class UserForm(forms.ModelForm):

    contact = forms.ModelChoiceField(
        queryset=Contact.objects.get_queryset(),
        label=ugettext_lazy('Contact'),
        help_text=ugettext_lazy('''
            Select the contact that will be bound to this user. 
            You can only choose from volunteers marked as contacts.
        '''),
        required=True,
        widget=select2.ModelSelect2Widget(
            model=Contact,
            search_fields=['name__icontains'],
            queryset=Contact.objects.filter(
                tags__tag_type__in=['vo'], user_link=None
            ),
        ),
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'groups']
        labels = {
            'username' : ugettext_lazy('Username'),
            'password' : ugettext_lazy('Password'),
            'groups'   : ugettext_lazy('Permission Groups'),
        }
        widgets = {
            'password': forms.PasswordInput(),
            'groups' : select2.ModelSelect2MultipleWidget(
                model=Group,
                search_fields=['name__icontains']
            ),
        }

    def update_user_contact(self):        
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        contact = self.cleaned_data['contact']
        groups = self.cleaned_data['groups']

        new_user = User.objects.create_user(
            username=username, password=password,
            email=contact.email
        )

        new_user.save()
        contact.user_link = new_user
        contact.save()

        for grp in groups:
            print(grp.name)
            grp.user_set.add(new_user)
            grp.save()