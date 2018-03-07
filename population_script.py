
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'barkwithfriends.settings')
import django
django.setup()
from bark.models import User, Organizer, DogOwner, Event, FoodMenu, Rating, ChooseAnEvent


def populate():


    def add_event(title,theme,capacity,date,start,end):
        c = Event.objects.get_or_create(title=title,theme=theme,capacity=capacity,date=date,start=start,end=end)[0]
        c.theme=theme
        c.capacity = capacity
        c.date=date
        c.start=start
        c.end=end
        c.save()
        return c


    if __name__ == '__main__':
        print("Starting Bark population scripts...")
        populate()