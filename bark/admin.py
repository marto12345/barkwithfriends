from django.contrib import admin

# Register your models here.
from bark.models import UserProfile, Event, FoodMenu, Rating, ChooseAnEvent
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(FoodMenu)
admin.site.register(Rating)
admin.site.register(ChooseAnEvent)

