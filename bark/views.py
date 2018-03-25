from bark.forms import addEventForm,UserForm,addRatingForm,UserUpdateForm,ResetForm,OwnerForm,OrganizerForm
from django.shortcuts import render
from bark.models import Event,UserProfile,Rating
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from bark.decorators import owner_required,organizer_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from datetime import datetime, timedelta, time,date
from django.db.models import Q
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

#gets rid for all previous events and returns the first 10 upcoming
def show_upcoming_events():
    today = date.today()  # get today`s date
    return Event.objects.filter(Q(date__gte=today)).order_by('date')[:10]  # display closest 10 events

#The index view: upcoming events ordered by closest date first
def index(request):
    event_list=show_upcoming_events()
    context_dict = {'events': event_list} #put these in a context dict
    return render(request,'index.html', context_dict,)

#about view:entirely based on template file
def about(request):
    return render(request,'about.html')

#food menu view:entirely based on template file
def food_menu(request):
    return render(request,'food-menu.xml')

#contact us view: entirely based on template file
def contact(request):
    return render(request,'contact.html')


#events form view : visible for owners only (i.e. neither for organizer nor for admin user)
@login_required
@user_passes_test(lambda u: not u.is_superuser)
@owner_required
def events(request):
        event_list = show_upcoming_events()
        context_dict = {'events':event_list}
        checked_ev=request.GET.getlist('checks')#get all events selected by owner
        for chosen in checked_ev:
            #store these in a list
            events_list=request.user.userprofile.events
            #if user has already signed for this one display:
            if chosen in events_list:
                messages.warning(request,'''You are not allowed to sign for the same event twice!
                If you have another pet you wish to bring , you need to create another account!
                ''')
            else:
                #get the event and date
                event_date=Event.objects.get(title=chosen).date
                event_time=Event.objects.get(title=chosen).start
                #format these nicely and append to events char field of user
                events_list+=("%s"%event_date)+":"+"---"+chosen+"---Start:"+("%s"%(event_time))+";"
                #update user`s events field and save
                request.user.userprofile.events=events_list
                request.user.userprofile.save()
                #for every chosen event decrease event capacity
                for event in event_list:
                 if event.title==chosen:
                        event.capacity-=1
                        event.save()
        return render(request,'events.html',context_dict)

#restricted view used when user is trying to access a restricted for them page
@login_required
def restricted(request):
    return render(request,'restricted.html')

#add event view: can only be accessed by organizer ( not admin and not owner)
@login_required
@user_passes_test(lambda u: not u.is_superuser)
@organizer_required
def add_event(request):
    #use the addEventForm:
    form = addEventForm()
    #get the request from user into the form:
    if request.method == 'POST':
        form = addEventForm(request.POST)

    # Have we been provided with a valid form?
        if form.is_valid():
            #get the organizer first and last time to display in events and home
            org = request.user.first_name +" "+ request.user.last_name
            form.organizerusername=org

            #get the selected date for event in right format:
            string_input_with_date=str(request.POST.get('date'))
            taken = datetime.strptime(string_input_with_date, "%m/%d/%Y")

           #check if it is already taken and if so display an error message
            if Event.objects.filter(date=taken.date()):
                messages.error(request, "This date is taken! Please choose another date and refill and recheck your event start and end times")
            #if everything is ok , save the event
            else:
                event= form.save(commit=True)
                e = Event.objects.get(title=event.title)
                pic=request.FILES.get("event_picture")
                e.event_picture=pic
                e.organizerusername=org
                e.save()
                #after a succesfully added event, go back to index page
                return redirect('index')
        else:
            print(form.errors)

    return render(request,'add-event.html', {'form': form})

#calculates the number of ratings and frequnecy of giving votes for each organizer
def calculate_rating(username):

    rating_freq = {1:0, 2:0, 3:0, 4:0, 5:0}
    reviews_num=0
    try:
        for rating in Rating.objects.filter(organizername=username):
                rating_freq[rating.starvalue] += 1
                reviews_num+=1
    except:
        pass

    return rating_freq,reviews_num

#checks whether a rating already exists
def rating_exists(rating):
    owner=rating.ownername
    org=rating.organizername
    for r in Rating.objects.filter(ownername=owner):
        if r.organizername==org:
            return r
    return rating

#the view ratings page can be seen by everyone except for admin user (who can actually edit these in the admin page)
@login_required
@user_passes_test(lambda u: not u.is_superuser)
def view_ratings(request):
    context_dict={"organizers":[]}
    org_list = UserProfile.objects.filter(is_organizer=True)
    context_dict["organizers"]=org_list

    return render(request,'view-ratings.html',context_dict)

#ratings view: accessed only by owners
@login_required
@user_passes_test(lambda u: not u.is_superuser)
@owner_required
def ratings(request,organizer_str):
    owner_user=User.objects.get(username=request.user.username)
    owner = UserProfile.objects.get(user=owner_user)
    context_dict = {'rates': {}, 'form': {},'organizer_user':organizer_str,'owner_user':owner,"reviews":0}

    organizer_user = User.objects.get(username=organizer_str)
    organizer = UserProfile.objects.get(user= organizer_user)
    comments=[]
    for r in Rating.objects.filter(organizername=organizer)[:5]:
        comments.append(r.comment)
    context_dict['comments']=comments;
    context_dict['avg']=organizer.avgrating

    rates,reviews = calculate_rating(organizer)
    context_dict["reviews"]=reviews
    context_dict['rates'] = rates
    context_dict['organizer_user']=organizer

    return render(request,'ratings.html',context_dict)

def rate_ajax(request, organizer_str):

    owner_user=User.objects.get(username=request.user.username)
    owner = UserProfile.objects.get(user=owner_user)

    context_dict = {'rates': {}, 'form': {}, "reviews": 0}

    print ('owner %s' % owner)

    organizer_user = User.objects.get(username=organizer_str)
    organizer = UserProfile.objects.get(user=organizer_user)

    context_dict['avg'] = organizer.avgrating
    print('avg1')
    print(organizer.avgrating)

    c = Rating()
    starvalue=request.GET['star_value']
    comment=request.GET['comment']

    c.starvalue=starvalue
    c.comment=comment
    c.ownername = owner
    c.organizername = organizer
    c = rating_exists(c)

    c.starvalue = starvalue
    c.comment = comment
    c.save()
    context_dict['avg'] = c.organizername.avgrating
    print ('obj %s' % c)
    print('avg2')
    print(organizer.avgrating)
    comments = []
    for r in Rating.objects.filter(organizername=organizer)[:5]:
        comments.append(r.comment)
    context_dict['comments'] = comments;

    context_dict['star_value'] = c.starvalue;
    rates, reviews = calculate_rating(organizer)
    context_dict["reviews"] = reviews
    context_dict['rates'] = rates


    return JsonResponse(context_dict)

@login_required
@user_passes_test(lambda u: not u.is_superuser)
@owner_required
def add_rating(request):
    context_dict = {"Organizers": []}
    if request.method == 'GET':
        org_list = UserProfile.objects.filter(is_organizer=True)
        context_dict["Organizers"] = org_list

    return render(request, 'add-rating.html', context_dict)


#register view from which register as owner and register as organizer will be accessible form
def register(request):
    return render(request,'register.html')

#login view
def user_login(request):
    if request.method == 'POST':
        #get the username and password from form and authenticate the user
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        #as long as the account is still active , log the user in
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:

               return HttpResponse("Your account is disabled.")
        #otherwise details provided are invalid:
        else:
            return render(request, 'invalidlogin.html')
    else:

        return render(request, 'login.html')



@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
    logout(request) # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

#register as owner view
def register_owner(request):
        registered = False #indicates whether user has already registered
        if request.method == 'POST':
            #create the user form and user profile form
            user_form = UserForm(request.POST)
            profile_form = OwnerForm(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                #ensure password is at least 6 char long
                if len(request.POST.get('password'))<6:
                    messages.error(request,"Password too short.Needs to be at least 6 characters long")
                else:
                    #set the user`s password and save
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    #if user has chosen to upload pictures manage these:
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
            if len(request.POST.get('password')) < 6:
                messages.error(request, "Password too short.Needs to be at least 6 characters long")
            # profile_form.is_owner = True
            else:
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



def reset_password(request):
    reset_pass={}
    if request.method=='POST':
        username = request.POST.get('username')
        user=User.objects.get(username=username)
        print(user)
        reset_pass=ResetForm(request.POST)

        if reset_pass.is_valid():
            if(UserProfile.objects.get(user=user).secret_question==reset_pass.cleaned_data["secret_question"]):
                print("yes")
                password = reset_pass.cleaned_data['password']
                print(password)
                user.password=make_password(password)
                print(user)
                user.save()
                print(user.password)
                return redirect('login')
            else:
                messages.error(request,"You have not answeted a valid answer for the secret question!")
    else:
         messages.error(request,"Something went wrong! Try again,please.")
    return render(request, 'reset-password.html',{'reset_pass':reset_pass })

def invalid_login(request):
    return render('invalidlogin.html')


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
                picture = profile.profile_picture
                profile.profile_picture = request.FILES.get('profile_picture',picture)
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

