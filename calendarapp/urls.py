from django.urls import path

from .views import etkinlik_views
from .views import uye_views
from .views import kort_views
from .views import antrenor_views
from .views import grup_views

app_name = "calendarapp"

urlpatterns = [
    # Etkinlik
    path("takvim/", etkinlik_views.takvim_getir, name="takvim-getir"),
    path("etkinlik/", etkinlik_views.ButunEtkinliklerListView.as_view(), name="getir_butun_etkinlikler"),
    path("etkinlik/bugun-devam-eden", etkinlik_views.BugunEtkinlikleriListView.as_view(),
         name="getir_bugun_devam_eden_etkinlikler"),
    path("etkinlik/gelecek", etkinlik_views.GelecekEtkinliklerListView.as_view(), name="getir_gelecek_etkinlikler"),

    path("etkinlik/detay", etkinlik_views.getir_etkinlik_bilgisi_ajax, name="getir_etkinlik_by_id"),
    path("etkinlik/sil", etkinlik_views.sil_etkinlik_ajax, name="sil_etkinlik_by_ajax"),
    path("etkinlik/sil/<int:id>", etkinlik_views.sil_etkinlik_ajax, name="sil_etkinlik_by_id"),
    path("etkinlik/serisi_sil", etkinlik_views.sil_etkinlik_serisi_ajax, name="sil_etkinlik_serisi_by_id"),
    path("etkinlik/kaydet", etkinlik_views.kaydet_etkinlik_ajax, name="kaydet_etkinlik_ajax"),
    path("etkinlik/tasi", etkinlik_views.saat_guncelle_etkinlik_ajax, name="saat_guncelle_etkinlik_ajax"),

    # Uye
    path("uye/index", uye_views.index_uye, name="index_uye"),
    path("uye/kaydet", uye_views.kaydet_uye, name="kaydet_uye"),
    path("uye/kaydet/<int:id>", uye_views.kaydet_uye, name="guncelle_uye"),
    path("uye/detay/<int:id>", uye_views.detay_uye, name="detay_uye"),
    path("uye/sil/<int:id>", uye_views.sil_uye, name="sil_uye"),

    # Kort
    path("kort/index", kort_views.index_kort, name="index_kort"),
    path("kort/kaydet", kort_views.kaydet_kort, name="kaydet_kort"),
    path("kort/detay/<int:id>", kort_views.detay_kort, name="detay_kort"),

    # Antrenor
    path("antrenor/index", antrenor_views.index_antrenor, name="index_antrenor"),
    path("antrenor/kaydet", antrenor_views.kaydet_antrenor, name="kaydet_antrenor"),
    path("antrenor/detay/<int:id>", antrenor_views.detay_antrenor, name="detay_antrenor"),

    # Grup
    path("grup/index", grup_views.index_grup, name="index_grup"),
    path("grup/detay/<int:id>", grup_views.detay_grup, name="detay_grup"),

]
