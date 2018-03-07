from django.db import models
from django import forms
from bark.models import Event

class addEventForm(forms.ModelForm):


    class Meta:  # Provide an association between the ModelForm and a model

        model = Event
        exclude = ('organizerusername',)