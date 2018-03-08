from django.db import models
from django import forms
from bark.models import Event,User,DogOwner,Organizer
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class addEventForm(forms.ModelForm):


    class Meta:  # Provide an association between the ModelForm and a model

        model = Event
        exclude = ('organizerusername',)

class OwnerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    dogname = models.CharField(max_length=128)
    dog_picture = models.ImageField(upload_to='profile_images', blank=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields={'username','first_name','last_name','description','email','profile_picture'}

