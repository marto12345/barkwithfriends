
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'barkwithfriends.settings')
import django
django.setup()
from django.contrib.auth.models import User
from bark.models import UserProfile, Event, FoodMenu, Rating, ChooseAnEvent

def add_user(username,email,password,first,last):
    user = User.objects.create_user(username,email,password,first_name=first,last_name=last)
    user.save()
    return user

def add_userprofile(user,description,profile_picture,dog_picture,dog_name,is_organizer,is_owner):
    userprofile = UserProfile.objects.get_or_create(user=user,description=description,
                                                    profile_picture=profile_picture,dog_picture=dog_picture,dog_name=dog_name,is_organizer=is_organizer,is_owner=is_owner)[0]


def populate():
    owner = add_user("owner","marto12345@abv.bg","parola","Martin","Dimitrov")
    owner.save()
    organizer = add_user("organizer","marto12345@abv.bg","parola","Martin","Dimitrov")
    organizer.save()
    Owner = add_userprofile(owner,"123","default/person.jpg","default/dog.jpg","Fifo",False,True)
    Organizer = add_userprofile(organizer,"123","default/person.jpg","default/dog.jpg","Fifo",True,False)
   # Owner.save()
    #Organizer.save()
    
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
