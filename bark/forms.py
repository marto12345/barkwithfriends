from django.db import models
from django import forms
from django.contrib.auth.models import User
from bark.models import Event,UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class addEventForm(forms.ModelForm):


    class Meta:  # Provide an association between the ModelForm and a model

        model = Event
        fields={'title','theme','capacity','date','start','end'}
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'}),'start': forms.TimeInput(attrs={'id': 'start'})
       , 'end': forms.TimeInput(attrs={'id': 'end'})}

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name','last_name' ,'email', 'password')
class OwnerForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields = ('profile_picture','dog_name', 'dog_picture')

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)