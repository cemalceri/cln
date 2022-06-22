from django.urls import path

from .views import etkinlik_views as views

app_name = "calendarapp"

urlpatterns = [
    # Etkinlik
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/", views.RunningEventsListView.as_view(), name="running_events"),

    path("takvim/", views.takvim_getir, name="takvim-getir"),
    path("etkinlik/detay", views.getir_etkinlik_bilgisi_ajax, name="getir_etkinlik_by_id"),
    path("etkinlik/sil", views.sil_etkinlik_ajax, name="sil_etkinlik_by_id"),
    path("etkinlik/serisi_sil", views.sil_etkinlik_serisi_ajax, name="sil_etkinlik_serisi_by_id"),
    path("etkinlik/kaydet", views.kaydet_etkinlik_ajax, name="kaydet_etkinlik_ajax"),

]
