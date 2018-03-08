from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    description = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    is_organizer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

class Organizer(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avgrating = models.IntegerField(validators = [MinValueValidator(0),
                                       MaxValueValidator(5)])

    class Meta:
        verbose_name_plural = 'Users/Organizers'


class DogOwner(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dogname = models.CharField(max_length=128)
    dog_picture= models.ImageField(upload_to='profile_images', blank=True)

    class Meta:
        verbose_name_plural = 'Users/DogOwners'


class Event(models.Model):
    title = models.CharField(max_length=128,unique=True)
    theme = models.CharField(max_length=128)
    capacity = models.IntegerField(validators=[MinValueValidator(1),
                                               MaxValueValidator(25)])
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()


    organizerusername = models.ForeignKey(Organizer)

    class Meta:
        verbose_name_plural = 'Events'

    def save(self, *args, **kwargs):


        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


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
