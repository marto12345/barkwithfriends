from bark.forms import addEventForm
from django.shortcuts import render
from bark.models import Event


def index(request):

    event_list = Event.objects.order_by('-date')[:10]
    context_dict = {'events': event_list}

    return render(request,'index.html', context_dict)

def about(request):
    return render(request,'about.html')

def food_menu(request):
    return render(request,'food-menu.html')

def contact(request):
    return render(request,'contact.html')

def events(request):
    return render(request,'events.html')

def show_event(request,event_title):
    context_dict = {}
    try:
        event = Event.objects.get(title=event_title)
        context_dict['event'] = event
    except Event.DoesNotExist:context_dict['event'] = None
    return render(request, 'bark/add-event.html', context_dict)


#@login_required
def add_event(request):
    form = addEventForm()

    # A HTTP POST?
    if request.method == 'POST':
        title = request.POST.get('title')
        theme = request.POST.get('theme')
        capacity = request.POST.get('capacity')
        date = request.POST.get('date')
        start = request.POST.get('start')
        end = request.POST.get('end')
        form = addEventForm(data=request.POST)
    # Have we been provided with a valid form?

        if form.is_valid(): # Save the new category to the database.
            event= form.save()
            return index(request)
        else:
            print(form.errors)

    return render(request,'add-event.html', {'form': form})

def ratings(request):
    return render(request,'ratings.html')

#@login_required
def add_rating(request):
    return render(request,'add-rating.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

#@login_required
def myaccount(request):
    return render(request,'myaccount.html')

#@login_required
def logout(request):
    return render(request,'index.html')
