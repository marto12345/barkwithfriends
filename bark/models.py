from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=12)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    picture = models.ImageField()

class Organizer(User):
    avgrating = models.IntegerField(validators = [MinValueValidator(0),
                                       MaxValueValidator(5)])
class DogOwner(User):
    dogname = models.CharField(max_length=128)

class Event(models.Model):
    title = models.CharField(max_length=128,unique=True)
    date = models.DateField()
    time = models.TimeField()
    capacity = models.IntegerField(validators = [MinValueValidator(1),
                                       MaxValueValidator(30)])
    theme = models.CharField(max_length=128)
    organizerusername = models.ForeignKey(Organizer)

class FoodMenu(models.Model):
    starter = models.CharField(max_length=128)
    mainCourse = models.CharField(max_length=128)
    dessert = models.CharField(max_length=128)
    ident = models.IntegerField(unique=True)
    drink = models.CharField(max_length=128)
    etitle = models.OneToOneField(Event,related_name='etitle')
    etime=models.OneToOneField(Event,related_name='etime')
    edate = models.OneToOneField(Event,related_name='edate')
    organizerusername = models.ForeignKey(Organizer)

class Rating(models.Model):
    starvalue = models.IntegerField(validators = [MinValueValidator(1),
                                       MaxValueValidator(5)])
    ident = models.IntegerField()
    comment = models.CharField(max_length=128)
    ownername = models.ForeignKey(DogOwner,related_name='ownername')
    organizeruser = models.ForeignKey(Organizer,related_name='organizeruser')

class ChooseAnEvent(models.Model):
    ownerusername = models.ForeignKey(DogOwner,related_name='ownerusername')
    eventtitle = models.ForeignKey(Event,related_name='eventtitle')
    eventdate = models.ForeignKey(Event,related_name='eventdate')
    time = models.ForeignKey(Event)
