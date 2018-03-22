from bark.forms import addEventForm,UserForm,addRatingForm,UserUpdateForm
from django.shortcuts import render
from bark.models import Event,UserProfile,Rating
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.http import HttpResponse
from bark.forms import OwnerForm,OrganizerForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from bark.decorators import owner_required,organizer_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from datetime import datetime, timedelta, time
from datetime import date
from django.db.models import Q
from datetime import datetime

def index(request):

    today =date.today()
    event_list = Event.objects.filter(Q(date__gte=today)).order_by('date')[:10]
    context_dict = {'events': event_list}

    return render(request,'index.html', context_dict,)

def about(request):
    return render(request,'about.html')

def food_menu(request):
    return render(request,'food-menu.xml')

def contact(request):
    return render(request,'contact.html')

@login_required
@owner_required
def events(request):


    #today = datetime.now().date()
    #event_list = Event.objects.order_by('date')
    today =date.today()
    event_list = Event.objects.filter(Q(date__gte=today)).order_by('date')
    context_dict = {'events':event_list}
    #for event in event_list:
        #if event.capacity==0:
              #  del context_dict[event]
    print(request)
    some_var=request.GET.getlist('checks')

    for chosen in some_var:
        events_list=request.user.userprofile.events
        if chosen in events_list:
            messages.warning(request,'''You are not allowed to sign for the same event twice!
            If you have another pet you wish to bring , you need to create another account!
            
            ''')
        else:
            event_date=Event.objects.get(title=chosen).date
            event_time=Event.objects.get(title=chosen).start

            events_list+=("%s"%event_date)+":"+"---"+chosen+"---Start:"+("%s"%(event_time))+";"
            request.user.userprofile.events=events_list
            request.user.userprofile.save()
            print( request.user.userprofile.events)

            for event in event_list:
             if event.title==chosen:
                    event.capacity-=1
                    event.save()
    return render(request,'events.html',context_dict)

def show_event(request,event_title):
    context_dict = {}
    try:
        event = Event.objects.get(title=event_title)
        context_dict['event'] = event
    except Event.DoesNotExist:context_dict['event'] = None
    return render(request, 'bark/add-event.html', context_dict)

@login_required
def restricted(request):
    return render(request,'restricted.html')


@login_required
@organizer_required
def add_event(request):


    form = addEventForm()

    # A HTTP POST?
    if request.method == 'POST':

        form = addEventForm(request.POST)

    # Have we been provided with a valid form?



        if form.is_valid(): # Save the new category to the database.
            org = request.user.first_name +" "+ request.user.last_name
            form.organizerusername=org
            print(form)
            #event_list = Event.objects.filter(request.POST.get('date'))
            string_input_with_date=str(request.POST.get('date'))
            past = datetime.strptime(string_input_with_date, "%m/%d/%Y")
            print(past.date())

            if Event.objects.filter(date=past.date()):
                messages.error(request, "This date is taken! Please choose another date and refill and recheck your event start and end times")

            else:
                event= form.save(commit=True)
                e = Event.objects.get(title=event.title)
                pic=request.FILES.get("event_picture")
                e.event_picture=pic
                e.organizerusername=org
                e.save()
                print(form)

                return redirect('index')

        else:
            print(form.errors)

    return render(request,'add-event.html', {'form': form})


def calculate_rating(username):

    rating_freq = {1:0, 2:0, 3:0, 4:0, 5:0}
    #print('smqtam')
    #print(rates[1])
    reviews_num=0
    try:
        for rating in Rating.objects.filter(organizername=username):
                rating_freq[rating.starvalue] += 1
                reviews_num+=1
    except:
        pass

    return rating_freq,reviews_num

def rating_exists(rating):
    owner=rating.ownername
    org=rating.organizername
    for r in Rating.objects.filter(ownername=owner):
        if r.organizername==org:
            return r
    return rating
@login_required
def view_ratings(request):
    context_dict={"organizers":[]}
    org_list = UserProfile.objects.filter(is_organizer=True)
    context_dict["organizers"]=org_list

    return render(request,'view-ratings.html',context_dict)

@login_required
@owner_required
def ratings(request,organizer_str):
    owner_user=User.objects.get(username=request.user.username)
    owner = UserProfile.objects.get(user=owner_user)
    #print("orgvjhbhbjhbjh")
  # print(owner)
    context_dict = {'rates': {}, 'form': {},'organizer_user':organizer_str,'owner_user':owner,"reviews":0}
   # print(organizer)
    #print(type(organizer))
    #name = request.POST.get('organizername')
    # form = addRatingForm(request.GET)
    organizer_user = User.objects.get(username=organizer_str)
    organizer = UserProfile.objects.get(user= organizer_user)
  # print("organizer")
    #print(organizer)

    #print(type(name))
    # form.organizername=name
    # context_dict['form'] = form
    rates,reviews = calculate_rating(organizer)
    context_dict["reviews"]=reviews
    context_dict['rates'] = rates
  #for k,v in rates.items():
       #print(k, v)
    context_dict['organizer_user']=organizer
    if request.method == 'POST':
        # print('ohhhh')
        #print(request.POST)
        form = addRatingForm(request.POST)
        context_dict['form'] = form
        if form.is_valid():
            rating = form.save(commit=False)
            rating.ownername = owner
            rating.organizername=organizer
            rating = rating_exists(rating)
            rating.starvalue=form.cleaned_data['starvalue']
            rating.comment=form.cleaned_data['comment']
            rating.save()

            #return HttpResponse("Successfully added a rating!");
            #return index(request)
            return render(request, 'ratings.html', context_dict)

        else:
            print(form.errors)
    else:
        form = addRatingForm()
        context_dict['form'] = form

    return render(request,'ratings.html',context_dict)


@login_required
@owner_required
def add_rating(request):
    context_dict = {"Organizers": []}
    if request.method == 'GET':
        org_list = UserProfile.objects.filter(is_organizer=True)
        context_dict["Organizers"] = org_list

    # for org in org_list:
    #   print("hop")
    #  print(org)
    # print(type(org))

    # context_dict={}

    # org_list = UserProfile.objects.filter(is_organizer=True)

    return render(request, 'add-rating.html', context_dict)

'''
@login_required
@owner_required
def add_rating(request):
    context_dict = {"Organizers": []}
    if request.method == 'GET':
          org_list = UserProfile.objects.filter(is_organizer=True)
          context_dict["Organizers"] = org_list
    
   # for org in org_list:
    #   print("hop")
     #  print(org)
       #print(type(org))

    #context_dict={}

    #org_list = UserProfile.objects.filter(is_organizer=True)



    return render(request,'add-rating.html',context_dict)
'''


def register(request):
    return render(request,'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        #print (user.userprofile.is_owner)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request, 'login.html')



@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
    logout(request) # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))


def register_owner(request):
        registered = False
        if request.method == 'POST':

            user_form = UserForm(request.POST)
            profile_form = OwnerForm(request.POST)

            #print (profile_form.is_valid())
            #print ("asd" + str(dir(profile_form)))
            #print (profile_form.profile_picture)
            if user_form.is_valid() and profile_form.is_valid():
                #profile_form.is_owner = True
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
               # print (profile.is_owner)
                profile.user = user
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                if 'dog_picture' in request.FILES:
                    profile.dog_picture = request.FILES['dog_picture']
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
                profile.profile_picture = request.FILES['profile_picture']
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

#def foo(is_organiser)
#    return Owener if is_organiser else Oth

@login_required

def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if request.user.userprofile.is_owner:
            profile_form = OwnerForm(request.POST, instance=request.user.userprofile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile = profile_form.save(commit=False)
                picture = profile.profile_picture
                profile.profile_picture = request.FILES.get('profile_picture', picture)

                dog_picture = profile.dog_picture
                profile.dog_picture = request.FILES.get('dog_picture', dog_picture)
                profile.save()
                profile_form.save()
                print('Your profile was successfully updated!')
            return redirect('update-profile')
        elif request.user.userprofile.is_organizer:
            profile_form = OrganizerForm(request.POST, request.FILES, instance=request.user.userprofile)
            #profile = profile_form.save(commit=False)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile = profile_form.save(commit=False)
                profile.profile_picture = request.FILES.get('profile_picture')
                profile.save()
                profile_form.save()
                print('Your profile was successfully updated!')
            return redirect('update-profile')

        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        if request.user.userprofile.is_organizer==True:
                profile_form = OrganizerForm(instance=request.user.userprofile)
        if request.user.userprofile.is_owner==True:
                profile_form = OwnerForm(instance=request.user.userprofile)
    return render(request, 'update-profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

