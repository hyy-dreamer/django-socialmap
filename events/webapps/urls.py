"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('venues', views.all_venues, name="list-venues"),
    path('add_venue', views.add_venue, name="add-venue"),
    path('show_venue/<venue_id>', views.show_venue, name="show-venue"),
    path('search_venues', views.search_venues, name="search-venues"),
    path('update_venue/<venue_id>', views.update_venue, name="update-venue"),
    path('add_event', views.add_event, name="add-event"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete-venue"),
    path('venue_text/<venue_id>', views.venue_text, name="venue-text"),
    path('event_pdf', views.event_pdf, name="event-pdf"),
    path('get_location', views.get_location, name="get-location"),
    path('login_user', views.login_user, name="login-user"),
    path('logout_user', views.logout_user, name="logout-user"),
    path('register_user', views.register_user, name="register-user"),
]

admin.site.site_header = "CMU Social Map Administration Page"
admin.site.site_title = "Social Map"
admin.site.index_title = "Welcome to Admin Area"
