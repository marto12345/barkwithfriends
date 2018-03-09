
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'barkwithfriends.settings')
import django
django.setup()
from bark.models import UserProfile, Event, FoodMenu, Rating, ChooseAnEvent

def populate():
    dog_events = [
        {"title": "Disco Party",
         "theme": "80s",
         "capacity": "12",
         "date":"2018-03-29",
         "start":"16:30:00",
         "end":"20:30:00"

    },
         {"title": "Hawaii party",
         "theme": "Coconut",
         "capacity": "18",
         "date": "2018-04-29",
         "start": "17:30:00",
         "end": "20:30:00"
    }
    ]


    for event in dog_events:

        c = add_event( event["title"], event["theme"],event["capacity"],event["date"],event["start"],event["end"])






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