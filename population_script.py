
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
         "end":"20:30:00",
         "organizerusername":"John Smith",
         "starter":"Tomato Soup",
         "main":"Pasta bolognese",
         "dessert":"Chocolate cake",
         "drink":"Espresso",
         "dog_food":"Beef stew"

    },
         {"title": "Hawaii party",
         "theme": "Coconut",
         "capacity": "18",
         "date": "2018-04-29",
         "start": "17:30:00",
         "end": "20:30:00",
        "organizerusername": "John Smith",
          "starter": "Tomato Soup",
          "main": "Pasta bolognese",
          "dessert": "Chocolate cake",
          "drink": "Espresso",
          "dog_food": "Beef stew"
    }
    ]


    for event in dog_events:

        c = add_event( event["title"], event["theme"],event["capacity"],event["date"],event["start"],event["end"],event["organizerusername"],
                       event["starter"],event["main"],event["dessert"],event["drink"],event["dog_food"])






def add_event(title,theme,capacity,date,start,end,organizerusername,starter,main,dessert,drink,dog_food):
        c = Event.objects.get_or_create(title=title,theme=theme,capacity=capacity,date=date,start=start,end=end,organizerusername=organizerusername,starter=starter,
          main=main,dessert=dessert,drink=drink,dog_food=dog_food)[0]
        c.theme=theme
        c.capacity = capacity
        c.date=date
        c.start=start
        c.end=end
        c.organizerusername=organizerusername
        c.starter=starter
        c.main=main
        c.dessert=dessert
        c.drink=drink
        c.dog_food=dog_food
        c.save()
        return c


if __name__ == '__main__':
        print("Starting Bark population scripts...")
        populate()