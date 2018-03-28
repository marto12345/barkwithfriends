from django.db import models
from django import forms
from django.contrib.auth.models import User
from bark.models import Event,UserProfile,Rating
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError


MAINS = (
    ('Toastie', 'Toastie with Cheese and Ham'),
    ('Chicken', 'Toast Chicken Baguette'),
    ('Pasta', 'Pasta bolognese'),
    ('Tofu', 'Tofu katsu curry'),
)
STARTERS = (

    ('TomSoup', 'Tomato soup'),
    ('Green', 'Greenveg Soup'),
    ('Falhum', 'Falafel and Hummus'),
    ('Olive', 'Olive sun dried tomato baguette'),
    ('Cheese','Cheese selection'),
)

DESSERTS= (

    ('Porridge', 'Oatmeal blueberry porridge '),
    ('Choc', 'Chocolate cake'),
    ('Crepe', 'Banana nutella crepe'),
)
DRINKS=(
    ('Espresso','Espresso' ),
    ('Cappuccino','Cappuccino'),
    ('Chai','Chai Latte'),
)
DOG=(
    ('Beef ','Beef stew ' ),
    ('Chicken','Chicken soup'),
    ('Chai','Chai Latte'),
    ('Cookies','Cookies'),
)

#add event form
class addEventForm(forms.ModelForm):
    starter = forms.ChoiceField(choices=STARTERS, label="", initial='', widget=forms.Select(), required=True)
    main = forms.ChoiceField(choices=MAINS, label="", initial='', widget=forms.Select(), required=True)
    dessert = forms.ChoiceField(choices=DESSERTS, label="", initial='', widget=forms.Select(), required=True)
    drink = forms.ChoiceField(choices=DRINKS, label="", initial='', widget=forms.Select(), required=True)
    dog_food = forms.ChoiceField(choices=DOG, label="", initial='', widget=forms.Select(), required=True)
    event_picture = forms.ImageField(help_text="Select a suitable image for your event", required=False)
    class Meta:  # Provide an association between the ModelForm and the Event model

        model = Event
        fields = {'title', 'theme', 'capacity', 'date', 'start', 'end','starter','main','dessert','drink','dog_food','event_picture'}
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'}), 'start': forms.TimeInput(attrs={'id': 'start'})
            , 'end': forms.TimeInput(attrs={'id': 'end'}), "organizerusername": forms.HiddenInput()}


#user form for registration
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User  # Provide an association between the ModelForm and the User model
        fields = ('username','first_name', 'last_name','email', 'password','confirm_password')
        widgets = {'username': forms.TextInput(attrs={'minlength': 5}),'email': forms.TextInput(attrs={'minlength': 8,'required':True}),
                   'first_name': forms.TextInput(attrs={'required': True}),'last_name': forms.TextInput(attrs={'required':True})}


#make sure passwords match
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match")

#user form used when updating one`s profile
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email')

#used for owner registration
class OwnerForm(forms.ModelForm):
    profile_picture = forms.ImageField(help_text="Select a profile image to upload.",required=False)
    dog_picture = forms.ImageField(help_text="Select a profile image to upload.",required=False)
    is_owner = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    events = forms.CharField(widget=forms.HiddenInput(), initial='',required=False)

    class Meta:
        model=UserProfile
        fields = ('description', 'profile_picture', 'dog_picture', 'dog_name','is_owner','events','secret_question')
        widgets = {'events': forms.HiddenInput(attrs={'id':'e'})}

#used for organizer registration
class OrganizerForm(forms.ModelForm):
    profile_picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    is_organizer = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    avgrating=forms.FloatField(widget=forms.HiddenInput(),initial=0.1)
    events = forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
#
    class Meta:
        model = UserProfile
        exclude=('dog_name','dog_picture','user','is_owner','avgrating','events',)

#used in forgotten password
class ResetForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput,required=True)
    secret_question = forms.CharField(label="What is your first pet's name?",required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=True)

    class Meta:
        model=UserProfile
        fields=('secret_question',)
#make sure passwords match:
    def clean(self):
        cleaned_data = super(ResetForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match")


class addRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = {'starvalue','comment'}

