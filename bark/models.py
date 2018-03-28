from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=128,unique=True,help_text="Event title:")
    theme = models.CharField(max_length=128,help_text="Event theme:")
    capacity = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(25) ],help_text="Guest capacity maximum:25")
    date = models.DateField(blank=True,help_text="Event date:")
    start = models.TimeField(help_text="Start time:")
    end = models.TimeField(help_text="End time:")
    organizerusername = models.CharField(max_length=128)
    starter=models.CharField(max_length=128)
    main=models.CharField(max_length=128)
    dessert=models.CharField(max_length=128)
    drink=models.CharField(max_length=128)
    dog_food=models.CharField(max_length=128)
    event_picture=models.ImageField(upload_to='event-images/', default='default/event.jpg',blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Events'

    def save(self, *args, **kwargs):

        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class UserProfile(models.Model):
    user=models.OneToOneField(User) #use model django user
    description = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_images/', default='default/person.jpg',blank=True,null=True)
    dog_picture = models.ImageField(upload_to='profile_images/', default='default/dog.jpg',blank=True,null=True)
    dog_name= models.CharField(max_length=128)
    #these will be used to tell which type of user is using the app
    is_organizer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    avgrating = models.FloatField(null=True,validators=[MinValueValidator(0),MaxValueValidator(5)],default=0)
    events=models.CharField(max_length=256)
    secret_question=models.CharField(max_length=128)
    def __str__(self):
        return self.user.username

class FoodMenu(models.Model):
    starter = models.CharField(max_length=128)
    mainCourse = models.CharField(max_length=128)
    dessert = models.CharField(max_length=128)
    ident = models.IntegerField(unique=True)
    drink = models.CharField(max_length=128)
    etitle = models.OneToOneField(Event,related_name='etitle')
    etime=models.OneToOneField(Event,related_name='etime')
    edate = models.OneToOneField(Event,related_name='edate')


class Rating(models.Model):
    starvalue = models.IntegerField(validators = [MinValueValidator(1),MaxValueValidator(5)])

    ident=models.AutoField(primary_key=True)
    comment = models.CharField(max_length=128)
    ownername = models.ForeignKey(UserProfile,related_name='ownername')

    organizername = models.ForeignKey(UserProfile,related_name='organizername')


    class Meta:
        verbose_name_plural = 'Ratings'

    def save(self, *args, **kwargs):

        super(Rating, self).save(*args, **kwargs)

        sum=0
        num=0

        for rate in Rating.objects.filter(organizername=self.organizername):

            sum=sum+rate.starvalue
            num+=1

        avg=round(sum/num,2)

        self.organizername.avgrating = avg
        print(self.organizername.avgrating)
        self.organizername.save()



    def __str__(self):
        return 'Rating: {}'.format(self.ident)


class ChooseAnEvent(models.Model):
    ownerusername = models.ForeignKey(UserProfile,related_name='ownerusername')
    eventtitle = models.ForeignKey(Event,related_name='eventtitle')
    eventdate = models.ForeignKey(Event,related_name='eventdate')
    time = models.ForeignKey(Event)

