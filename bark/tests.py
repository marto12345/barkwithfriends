from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
import os
from django.contrib.auth.models import User
from bark.forms import UserForm,OwnerForm,OrganizerForm
from bark.models import UserProfile, FoodMenu, Event
from django.conf import settings
def create_user():
    # Create a user
    user = User.objects.get_or_create(username="testuser", password="test1234",
                                      first_name="Test", last_name="User", email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

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

class TemplateTests(TestCase):
    def test_base_template_exists(self):
        path_to_base = settings.TEMPLATE_DIR + '/base.html'
        print(path_to_base)
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
