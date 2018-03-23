from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
import os
from django.contrib.auth.models import User
from bark.forms import UserForm,OwnerForm,OrganizerForm
from bark.models import UserProfile, FoodMenu, Event
from django.conf import settings
client = Client()
def create_user():
    # Create a user
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


# Create your tests here.
class LoginTests(TestCase):
    def test_login_redirects_to_index(self):
        create_user()
        try:
            response = self.client.post(reverse('login)'),{'username': 'testuser', 'password': 'test1234'})
        except:
            try:
                response = self.client.post(reverse('bark:login'), {'username': 'testuser', 'password': 'test1234'})
            except:
                return False
        self.assertedRedirects(response,reverse('index'))

    def test_index_loads(self):
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code,200)

    def test_login_required(self):
        response = self.client.get(reverse('events'))
        self.assertRedirects(response,reverse('login')+"?next=/events",status_code=302,target_status_code=200)

    def test_owner_sees_events(self):
        owner = add_user("testowner","marto12345@abv.bg","parola","Martin","Dimitrov")
        owner.save()
        Owner = add_userprofile(owner,"123","default/person.jpg","default/dog.jpg","Fifo",False,True)
        client.login(username="testowner",password="parola")
        response = client.get(reverse('events'))
        self.assertEqual(response.status_code,200)

class TemplateTests(TestCase):
    def test_base_template_exists(self):
        path_to_base = settings.TEMPLATE_DIR + '/base.html'
        self.assertTrue(os.path.isfile(path_to_base))

    def test_link_to_index_in_base_template(self):
        response = self.client.get(reverse('index'))
        self.assertIn(reverse('index'), response.content.decode('ascii'))


    def test_index_displays_no_events_message(self):
        response = self.client.get(reverse('index'))
        self.assertIn("There are no events present.".lower(), response.content.decode('ascii').lower())

    def test_contact_page_using_template(self):
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
