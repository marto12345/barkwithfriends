from django.db import models
from django import forms
from bark.models import Event,User,DogOwner
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class addEventForm(forms.ModelForm):


    class Meta:  # Provide an association between the ModelForm and a model

        model = Event
        fields={'title','theme','capacity','date','start','end'}
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'}),'start': forms.TimeInput(attrs={'id': 'start'})
       , 'end': forms.TimeInput(attrs={'id': 'end'})}

class OwnerRegisterForm(UserCreationForm):
    dogname = models.CharField(max_length=128)
    dog_picture = models.ImageField(upload_to='profile_images', blank=True)
    class Meta(UserCreationForm.Meta):
        model = User
       # fields={'username','first_name','last_name','description','email','profile_picture'}
    @transaction.atomic
    def save(self):
        user = super(self).save(commit=False)
        user.is_owner = True
        user.save()
        student = Student.objects.create(user=user)
        return user
