from asyncio import events
from email.headerregistry import Address
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User


# Create a Venue model.
class Venue(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=360)
    zip_code = models.CharField(max_length=15)
    phone = models.CharField(max_length=25, blank=True)
    web = models.URLField(blank=True)
    email_address = models.EmailField(blank=True) 

    def __str__(self): #double underscores
        return self.name

# Create a user model.
class MyClubUser(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email_address = models.EmailField()
    def __str__(self):
        return self.first_name + ' ' + self.last_name



# Create a event class here.
class Event(models.Model):
    name = models.CharField(max_length=120)
    event_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True) # It is ok to leave this blank
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name