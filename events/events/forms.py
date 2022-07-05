from django import forms
from django.forms import ModelForm
from events.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"
        #fields = ('name', 'address'..)
        labels = {
            'name':'',
            'address': '',
            'zip_code':'',
            'phone':'',
            'web':'',
            'email_address':'',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Enther Zip Code'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Phone Number'}),
            'web':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Web Address'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}),
        }

# Create an event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        #fields = "__all__"
        fields = ('name', 'event_date','venue','manager','attendees','description')
        labels = {
            'name':'',
            'event_date': '',
            'venue':'',
            'manager':'',
            'attendees':'',
            'description':'',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Event Date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'Enther Venue'}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder':'Enter Manager'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-select','placeholder':'Enter attendees'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Description'}),
        }

# Create a registration form
class RegisterUserForm(UserCreationForm):#inheriate from UserCreationForm
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enther First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enther Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter Password Confirmation'
    