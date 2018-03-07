from django.contrib import admin

# Register your models here.
from bark.models import User, Organizer, DogOwner, Event, FoodMenu, Rating, ChooseAnEvent
admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(DogOwner)
admin.site.register(Event)
admin.site.register(FoodMenu)
admin.site.register(Rating)
admin.site.register(ChooseAnEvent)

