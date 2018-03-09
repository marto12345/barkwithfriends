from bark.forms import addEventForm
from django.shortcuts import render
from bark.models import Event,User,DogOwner
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from bark.forms import OwnerRegisterForm


def index(request):

    event_list = Event.objects.order_by('-date')[:10]
    context_dict = {'events': event_list}

    return render(request,'index.html', context_dict)

def about(request):
    return render(request,'about.html')

def food_menu(request):
    return render(request,'food-menu.xml')

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
        form = addEventForm(request.POST)
    # Have we been provided with a valid form?



        if form.is_valid(): # Save the new category to the database.
            event= form.save(commit=True)
            return HttpResponse("Successfully added an event!");
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

class register_owner(CreateView):
        model = User
        form_class = OwnerRegisterForm
        template_name = 'templates/organizer.html'

        def get_context_data(self, **kwargs):
            kwargs['user_type'] = 'owner'
            #return super().get_context_data(**kwargs)

        def form_valid(self, form):
            user = form.save()
            login(self.request, user)
            return redirect('index')
    # True when registration succeeds.
    #registered = False

    # If it's a HTTP POST, we're interested in processing form data.
   # if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    #  Note that we make use of both UserForm and UserProfileForm.
       # owner_form = OwnerRegisterForm(data=request.POST)
        #if owner_form.is_valid():

           # owner = owner_form.save()
            #owner.set_password(owner.password)
            #owner.save()

           # profile = owner_form.save(commit=False)
           # profile.user = owner
            #if 'profile_picture' in request.FILES:
            #    profile.profile_picture = request.FILES['profile_picture']
           # if 'dog_picture' in request.FILES:
            #    profile.dog_picture = request.FILES['picture']
        # Now we save the UserProfile model instance.
           # profile.save()

            #registered = True
       # else: # Invalid form or forms - mistakes or something else? # Print problems to the terminal.
           # print(owner_form.errors)
   # else:
      # owner_form = OwnerRegisterForm()
    # Render the template depending on the context.
    #return render(request, 'dogowner.html', {'owner_form': owner_form, 'registered': registered})



def register_organizer(request):
    return render(request,'organizer.html')
