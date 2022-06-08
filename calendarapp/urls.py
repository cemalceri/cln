from django.urls import path

from .views import rezervasyon_views as views

app_name = "calendarapp"

urlpatterns = [
    # Rezervasyon
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/", views.RunningEventsListView.as_view(), name="running_events"),

    path("takvim/", views.takvim_getir, name="takvim-getir"),
    path("rezervasyon/detay", views.getir_rezervasyon_bilgisi_ajax, name="getir_rezervasyon_bilgisi_by_id"),
    path("rezervasyon/sil", views.sil_rezervasyon_ajax, name="sil_rezervasyon_by_id"),
    path("rezervasyon/kaydet", views.kaydet_rezervasyon_ajax, name="kaydet_rezervasyon_ajax"),

]
