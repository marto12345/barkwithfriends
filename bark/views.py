from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


def food_menu(request):
    return render(request,'food-menu.html')

def contact(request):
    return render(request,'contact.html')

def events(request):
    return render(request,'events.html')

def add_event(request):
    return render(request,'add-event.html')

def ratings(request):
    return render(request,'ratings.html')

def add_rating(request):
    return render(request,'add-rating.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def myaccount(request):
    return render(request,'myaccount.html')

