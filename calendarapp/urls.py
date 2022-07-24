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
    path("takvim/<int:kort_id>", etkinlik_views.takvim_getir, name="takvim-getir_by_kort_id"),
    path("etkinlik/", etkinlik_views.ButunEtkinliklerListView.as_view(), name="getir_butun_etkinlikler"),
    path("etkinlik/bugun-devam-eden", etkinlik_views.BugunEtkinlikleriListView.as_view(),
         name="getir_bugun_devam_eden_etkinlikler"),
    path("etkinlik/gelecek", etkinlik_views.GelecekEtkinliklerListView.as_view(), name="getir_gelecek_etkinlikler"),

    path("etkinlik/detay", etkinlik_views.getir_etkinlik_bilgisi_ajax, name="getir_etkinlik_by_id"),
    path("etkinlik/sil", etkinlik_views.sil_etkinlik_ajax, name="sil_etkinlik_by_ajax"),
    path("etkinlik/sil/<int:id>", etkinlik_views.sil_etkinlik, name="sil_etkinlik_by_id"),
    path("etkinlik/serisi_sil", etkinlik_views.sil_etkinlik_serisi_ajax, name="sil_etkinlik_serisi_by_id"),
    path("etkinlik/kaydet", etkinlik_views.kaydet_etkinlik_ajax, name="kaydet_etkinlik_ajax"),
    path("etkinlik/tasi", etkinlik_views.saat_guncelle_etkinlik_ajax, name="saat_guncelle_etkinlik_ajax"),

    # Uye
    path("uye/index", uye_views.index_uye, name="index_uye"),
    path("uye/kaydet", uye_views.kaydet_uye, name="kaydet_uye"),
    path("uye/detay/<int:id>", uye_views.detay_uye, name="detay_uye"),
    path("uye/guncelle/<int:id>", uye_views.kaydet_uye, name="guncelle_uye"),
    path("uye/sil/<int:id>", uye_views.sil_uye, name="sil_uye"),

    # Kort
    path("kort/index", kort_views.index_kort, name="index_kort"),
    path("kort/kaydet", kort_views.kaydet_kort, name="kaydet_kort"),
    path("kort/detay/<int:id>", kort_views.detay_kort, name="detay_kort"),
    path("kort/guncelle/<int:id>", kort_views.kaydet_kort, name="guncelle_kort"),
    path("kort/sil/<int:id>", kort_views.sil_kort, name="sil_kort"),

    # Antrenor
    path("antrenor/index", antrenor_views.index_antrenor, name="index_antrenor"),
    path("antrenor/kaydet", antrenor_views.kaydet_antrenor, name="kaydet_antrenor"),
    path("antrenor/detay/<int:id>", antrenor_views.detay_antrenor, name="detay_antrenor"),
    path("antrenor/guncelle/<int:id>", antrenor_views.kaydet_antrenor, name="guncelle_antrenor"),
    path("antrenor/sil/<int:id>", antrenor_views.sil_antrenor, name="sil_antrenor"),

    # Grup
    path("grup/index", grup_views.index_grup, name="index_grup"),
    path("grup/kaydet", grup_views.kaydet_grup, name="kaydet_grup"),
    path("grup/detay/<int:id>", grup_views.detay_grup, name="detay_grup"),
    path("grup/guncelle/<int:id>", grup_views.kaydet_grup, name="guncelle_grup"),
    path("grup/sil/<int:id>", grup_views.sil_grup, name="sil_grup"),

]
