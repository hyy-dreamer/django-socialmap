from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from calendar import HTMLCalendar, month_name
from datetime import datetime

from socialmap.models import Profile, Event, Location
from socialmap.forms import EventForm

@login_required
def calendar(request,
         year=datetime.now().year,
         month=datetime.now().strftime('%B')):
    context = {}
    month = month.capitalize()
    #change the month string to month number
    month_number = list(month_name).index(month)
    month_number = int(month_number)

    #get a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    #get current time
    now = datetime.now()
    time = now.strftime('%I:%M:%S %p')

    context = {
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "time": time,
    }

    return render(request, 'socialmap/calendar.html', context)

@login_required
def home(request):
    return render(request, 'socialmap/map.html')

# Events related views
# Create event_list views 
def all_events(request):
    context = {}
    event_list = Event.objects.all().order_by('-event_date')
    context = {
        "event_list": event_list
    }
    return render(request, 'events/event_list.html', context)

# Create add event views
def add_event(request):
    context = {}
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/add_event', submitted=True)
    else: # need to fix redirect with success submit
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {"form": form, "submitted": submitted})

# Create update_event views
def update_event(request,event_id):
    context={}
    events = Event.objects.get(pk=event_id)
    if request.method == "POST":
        form = EventForm(request.POST,instance=events)
        if form.is_valid:
            form.save()
            return redirect('list-events')
    else:
        form = EventForm(instance=events)
        context = {
            "form": form
        }
        return render(request, 'events/update_event.html', context)

# Create delete_event views
def delete_event(request,event_id):
    events = Event.objects.get(pk=event_id)
    events.delete()
    return redirect('list-events')

@login_required
def test_action(request):
    return render(request, 'test/index.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('landing')