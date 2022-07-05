from inspect import ismethoddescriptor
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar, month_name
from datetime import datetime
from events.forms import EventForm, RegisterUserForm, VenueForm
from events.models import Event, Venue
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create calendar views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    context = {}
    month = month.capitalize()
    #change the month string to month number
    month_number = list(calendar.month_name).index(month)
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


    return render(request, 'events/home.html', context)

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
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
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


# Create all_venue views
def all_venues(request):
    context = {}
    # venue_list = Venue.objects.all().order_by('-name')
    venue_list = Venue.objects.all()
    p = Paginator(venue_list, 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    context = {
        "venue_list": venue_list,
        "venues": venues,
        "nums":nums,
    }
    return render(request, 'events/venue_list.html', context)

# Crate add_venue views
def add_venue(request):
    context = {}
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {"form": form, "submitted": submitted})

# Create show venue views
def show_venue(request, venue_id):
    context = {}
    venue = Venue.objects.get(pk=venue_id)
    context = {
        "venue": venue
    }
    return render(request, 'events/show_venue.html', context)

# Create search venue views 
def search_venues(request):
    context = {}
    if request.method == "POST":
        searched = request.POST["Searched"]
        venues = Venue.objects.filter(name__contains=searched)
        context = {
            "searched": searched,
            "venues": venues,
        }
        return render(request, 'events/search_venues.html', context)

    else: 
        return render(request, 'events/search_venues.html', context)


# Create update venue views
def update_venue(request, venue_id):
    context={}
    venues = Venue.objects.get(pk=venue_id)
    if request.method == "POST":
        form = VenueForm(request.POST,instance=venues)
        if form.is_valid:
            form.save()
            return redirect('list-venues')
    else:
        form = VenueForm(instance=venues)
        context = {
            "form": form
        }
        return render(request, 'events/update_venue.html', context)

# Create delete venue views
def delete_venue(request, venue_id):
    venues = Venue.objects.get(pk=venue_id)
    venues.delete()
    return redirect('list-venues')

def venue_text(request,venue_id):
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename=venue.txt' 
    venue = Venue.objects.get(pk=venue_id)
    lines = []
    lines.append(f'{venue}\n {venue.address}\n {venue.zip_code}\n {venue.phone}\n {venue.web}\n {venue.email_address}\n')
    response.writelines(lines)
    return response

def event_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)
    lines = []
    events = Event.objects.all()
    for event in events:
        lines.append("Event Name:" + event.name)
        #lines.append(event.event_date)
        lines.append("Venue Name:" + event.venue.name)
        # lines.append(event.manager)
        lines.append("Description:" + event.description)
        lines.append("========================================")
        # lines.append(event.attendees.all)
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='events.pdf')

def get_location(request):
    return render(request, 'events/my_location.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Pleased make sure you are registered!"))
            return redirect('login-user')
    else: return render(request, 'events/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('login-user')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ("Register successfully!"))
            return redirect('home')
        else: return render(request, 'events/register.html',{'form':form})
    else:
        form = RegisterUserForm()
        return render(request, 'events/register.html',{'form':form})

