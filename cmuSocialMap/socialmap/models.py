from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.

# Create a Profile model.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    friends = models.ManyToManyField(User, related_name='friends')


# Auto create Profile on User creation
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


# Create a Location model.
class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=360)
    zip_code = models.CharField(max_length=15)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True)
    web = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)

    def __str__(self): 
        return self.name


# Create a event class here.
class Event(models.Model):
    name = models.CharField(max_length=120)
    event_date = models.DateTimeField()
    location = models.ForeignKey(Location,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    manager = models.ForeignKey(User,
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL)
    description = models.TextField(blank=True)  # It is ok to leave this blank
    attendees = models.ManyToManyField(User, blank=True, related_name='attendees')

    def __str__(self):
        return self.name