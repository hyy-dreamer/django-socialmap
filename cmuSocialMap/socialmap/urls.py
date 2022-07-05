from django.urls import path
from socialmap import views

urlpatterns =[
    path('', views.home, name="home"),
    path('calendar', views.calendar, name="calendar"),
    path('events', views.all_events, name="list-events"),
    path('add_event', views.add_event, name="add-event"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('logout_user', views.logout_user, name="logout-user"),
]