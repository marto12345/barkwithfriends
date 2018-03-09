from bark.forms import addEventForm,UserForm,addRatingForm
from django.shortcuts import render
from bark.models import Event,UserProfile,Rating
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.http import HttpResponse
from bark.forms import OwnerForm,OrganizerForm


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
    if request.method == 'POST':
        form = addRatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=True)
            return HttpResponse("Successfully added an event!");
            return index(request)

        else:
            print(form.errors)
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


def register_owner(request):
        registered = False
        if request.method == 'POST':

            user_form = UserForm(request.POST)
            profile_form = OwnerForm(request.POST)


            if user_form.is_valid() and profile_form.is_valid():
                #profile_form.is_owner = True
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
               # print (profile.is_owner)
                profile.user = user
                if 'profile_picture' in request.FILES:
                    profile.picture = request.FILES['profile_picture']
                if 'dog_picture' in request.FILES:
                    profile.picture = request.FILES['dog_picture']
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = OwnerForm()
        return render(request, 'dogowner.html',
                      {'user_form': user_form, 'profile_form': profile_form,
                       'registered': registered})


def register_organizer(request):
    registered = False
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = OrganizerForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # profile_form.is_owner = True
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            # print (profile.is_owner)
            profile.user = user
            if 'profile_picture' in request.FILES:
                profile.picture = request.FILES['profile_picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = OrganizerForm()
    return render(request, 'organizer.html',
                  {'user_form': user_form, 'profile_form': profile_form,
                   'registered': registered})
