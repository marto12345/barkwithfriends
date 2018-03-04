Python 3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:04:45) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'barkwithfriends.settings')
import django
django.setup()
from barkwithfriends.models import User, Organizer, DogOwner, Event, FoodMenu, Rating, ChooseAnEvent
