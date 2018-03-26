from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import os
from django.contrib.auth.models import User
from bark.forms import UserForm,OwnerForm,OrganizerForm
from bark.models import UserProfile, FoodMenu, Event
from django.conf import settings
client = Client()
def create_user():
    # Create a custom test user
    user = User.objects.get_or_create(username="testuser", password="test1234",
                                      first_name="Test", last_name="User", email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

def add_user(username,email,password,first,last):
    user = User.objects.create_user(username,email,password,first_name=first,last_name=last)
    user.save()
    return user

def add_userprofile(user,description,profile_picture,dog_picture,dog_name,is_organizer,is_owner):
    userprofile = UserProfile.objects.get_or_create(user=user,description=description,
                                                    profile_picture=profile_picture,dog_picture=dog_picture,dog_name=dog_name,is_organizer=is_organizer,is_owner=is_owner)[0]

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    user_profile.save()

    return user, user_profile

def create_admin():
    User.objects.get_or_create(username="trialadmin", is_staff=True)
    user = User.objects.get(username="trialadmin")
    user.save()


# Create your tests here.
class LoginTests(TestCase):
    def test_login_redirects_to_index(self):
        create_user()
        try:
            #attempt to login
            response = self.client.post(reverse('login'),{'username': 'testuser', 'password': 'test1234'})
        except:
            try:
                response = self.client.post(reverse('bark:login'), {'username': 'testuser', 'password': 'test1234'})
            except:
                return False
        self.assertRedirects(response,reverse('index'))

    def test_index_loads(self):
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code,200)

    def test_login_required(self):
        response = self.client.get(reverse('events'))
        self.assertRedirects(response,reverse('login')+"?next=/events",status_code=302,target_status_code=200)

    def test_owner_sees_events(self):
        #create owner
        owner = add_user("testowner","marto12345@abv.bg","parola","Martin","Dimitrov")
        owner.save()
        Owner = add_userprofile(owner,"123","default/person.jpg","default/dog.jpg","Fifo",False,True)
        #login
        client.login(username="testowner",password="parola")
        response = client.get(reverse('events'))
        self.assertEqual(response.status_code,200)

    def test_organizer_sees_add_event(self):
        #create organizer
        organizer = add_user("testorganizer","marto12345@abv.bg","parola","Martin","Dimitrov")
        organizer.save()
        Organizer = add_userprofile(organizer,"123","default/person.jpg","default/dog.jpg","Fifo",True,False)
        #login
        client.login(username="testorganizer",password="parola")
        response = client.get(reverse('add-event'))
        self.assertEqual(response.status_code,200)

    def test_add_user(self):
        #check if a user's username is saved properly
        user = add_user("testuser","marto12345@abv.bg","parola","Martin","Dimitrov")
        user.save()
        TrialUser = add_userprofile(user,"123","default/person.jpg","default/dog.jpg","Pink",True,False)
        self.assertEqual(user.username=='testuser',True)

    def test_admin_tries_to_see_add_event(self):
        #createadmin account
        create_admin()
        response = self.client.get(reverse('add-event'))
        self.assertRedirects(response,reverse('login')+"?next=/add-event",status_code=302,target_status_code=200)

    def test_admin_tries_to_see_events(self):
        create_admin()
        response = self.client.get(reverse('events'))
        self.assertRedirects(response,reverse('login')+"?next=/events",status_code=302,target_status_code=200)
        

class TemplateTests(TestCase):
    def test_base_template_exists(self):
        path_to_base = settings.TEMPLATE_DIR + '/base.html'
        self.assertTrue(os.path.isfile(path_to_base))

    def test_link_to_index_in_base_template(self):
        response = self.client.get(reverse('index'))
        self.assertIn(reverse('index'), response.content.decode('ascii'))

    def test_index_displays_no_events_message(self):
        #check if a proper message is displayed
        response = self.client.get(reverse('index'))
        self.assertIn("There are no events present.".lower(), response.content.decode('ascii').lower())

    def test_contact_page_using_template(self):
        #check if base template is recognised
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response,'base.html')

class ModelTests(TestCase):
    def test_create_a_new_event(self):
        event = Event(title="Joanne",capacity=30,date="2018-03-29",start="17:30:00",end="20:00:00",organizerusername="Lady Gaga")
        event.save()
        # Check event is in database
        events_in_database = Event.objects.all()
        self.assertEquals(len(events_in_database), 1)
        only_event_in_database = events_in_database[0]
        self.assertEquals(only_event_in_database, event)

    def test_create_an_event_with_overlarge_capacity(self):
        #check if an event with huge capacity is not added
        event = Event(title="Pon De Replay",capacity=27,date="2018-03-29",start="17:30:00",end="20:00:00",organizerusername="Kylie")
        with self.assertRaises(ValidationError):
            if event.full_clean():
                event.save()
        self.assertEqual(Event.objects.filter(title="Pon De Replay").count(),0)
    
    def test_create_an_event_with_negative_capacity(self):
        #check if an event with negative capacity is not added
        event = Event(title="Pon De Replay",capacity=-20,date="2018-03-29",start="17:30:00",end="20:00:00",organizerusername="Kylie")
        with self.assertRaises(ValidationError):
            if event.full_clean():
                event.save()
        self.assertEqual(Event.objects.filter(title="Pon De Replay").count(),0)
