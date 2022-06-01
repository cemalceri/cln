from django.urls import path

from .views import rezervasyon_views as views

app_name = "calendarapp"

urlpatterns = [
    # Rezervasyon
    path("takvim/", views.TakvimView.as_view(), name="takvim-getir"),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    # path("add_eventmember/<int:event_id>", ov.add_eventmember, name="add_eventmember"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/", views.RunningEventsListView.as_view(), name="running_events"),
]
