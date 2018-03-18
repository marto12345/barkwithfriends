from django.db import models
from django import forms
from django.contrib.auth.models import User
from bark.models import Event,UserProfile,Rating
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class addEventForm(forms.ModelForm):

    class Meta:  # Provide an association between the ModelForm and a model

        model = Event
        fields={'title','theme','capacity','date','start','end'}
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'}),'start': forms.TimeInput(attrs={'id': 'start'})
       , 'end': forms.TimeInput(attrs={'id': 'end'}),"organizerusername":forms.HiddenInput()}

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email', 'password',)



class OwnerForm(forms.ModelForm):
    profile_picture = forms.ImageField(help_text="Select a profile image to upload.",required=False)
    dog_picture = forms.ImageField(help_text="Select a profile image to upload.",required=False)
    is_owner = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    events = forms.CharField(widget=forms.HiddenInput(), initial='',required=False)


    class Meta:
        model=UserProfile
        fields = ('description', 'profile_picture', 'dog_picture', 'dog_name','is_owner','events')
        widgets = {'events': forms.HiddenInput(attrs={'id':'e'})}

class OrganizerForm(forms.ModelForm):
    profile_picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    is_organizer = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    avgrating=forms.FloatField(widget=forms.HiddenInput(),initial=0.1)
    events = forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
#
    class Meta:
        # is_organizer = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
        model = UserProfile
        exclude=('dog_name','dog_picture','user','is_owner','avgrating','events')


class addRatingForm(forms.ModelForm):
    #frequency=forms.Field(widget=forms.HiddenInput(),initial=True)
    #CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    starvalue = forms.IntegerField(widget=forms.HiddenInput())
    comment = forms.CharField()
    #organizername=forms.CharField().disabled
    organizername = forms.CharField()
    ownername=forms.CharField(widget=forms.HiddenInput(),initial=User)
    class Meta:
        model = Rating
        fields = {'comment', 'organizername','starvalue','ownername'}


