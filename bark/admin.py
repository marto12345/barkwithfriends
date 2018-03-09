from django.contrib import admin

# Register your models here.
from bark.models import User,DogOwner, Event, FoodMenu, Rating, ChooseAnEvent
admin.site.register(User)

admin.site.register(DogOwner)
admin.site.register(Event)
admin.site.register(FoodMenu)
admin.site.register(Rating)
admin.site.register(ChooseAnEvent)

