from django.urls import path

from .views import etkinlik_views, rezervasyon_views, telafi_ders_views, abonelik_views
from .views import uye_views
from .views import kort_views
from .views import antrenor_views
from .views import grup_views
from .views import muhasebe_views

app_name = "calendarapp"

urlpatterns = [
    # Takvim
    path("takvim/", etkinlik_views.takvim_getir, name="takvim-getir"),
    path("takvim/<int:kort_id>", etkinlik_views.takvim_getir, name="takvim-getir_by_kort_id"),
    path("etkinlik/", etkinlik_views.ButunEtkinliklerListView.as_view(), name="getir_butun_etkinlikler"),
    path("etkinlik/bugun-devam-eden", etkinlik_views.BugunEtkinlikleriListView.as_view(),
         name="getir_bugun_devam_eden_etkinlikler"),
    path("etkinlik/gelecek", etkinlik_views.GelecekEtkinliklerListView.as_view(), name="getir_gelecek_etkinlikler"),

    # Etkinlik
    path("etkinlik/detay", etkinlik_views.getir_etkinlik_bilgisi_ajax, name="getir_etkinlik_by_id"),
    path("etkinlik/sil", etkinlik_views.sil_etkinlik_ajax, name="sil_etkinlik_by_ajax"),
    path("etkinlik/sil/<int:id>", etkinlik_views.sil_etkinlik, name="sil_etkinlik_by_id"),
    path("etkinlik/serisi-sil", etkinlik_views.sil_etkinlik_serisi_ajax, name="sil_etkinlik_serisi_by_id"),
    path("etkinlik/kaydet", etkinlik_views.kaydet_etkinlik_ajax, name="kaydet_etkinlik_ajax"),
    path("etkinlik/tasi", etkinlik_views.saat_guncelle_etkinlik_ajax, name="saat_guncelle_etkinlik_ajax"),
    path("etkinlik/tamamlandi", etkinlik_views.etkinlik_tamamlandi_ajax, name="etkinlik_tamamlandi_ajax"),
    path("etkinlik/katilim-ekle/<int:id>/<int:uye_id>", etkinlik_views.katilim_ekle,
         name="katilim_ekle_etkinlik"),
    path("etkinlik/iptal-et/<int:id>/<int:uye_id>", etkinlik_views.iptal_et,
         name="iptal_et_etkinlik"),
    path("etkinlik/iptal-geri-al/<int:id>/<int:uye_id>", etkinlik_views.iptal_geri_al,
         name="iptal_geri_al_etkinlik"),

    # Uye
    path("uye/index", uye_views.index, name="index_uye"),
    path("uye/kaydet", uye_views.kaydet, name="kaydet_uye"),
    path("uye/guncelle/<int:id>", uye_views.kaydet, name="guncelle_uye"),
    path("uye/sil/<int:id>", uye_views.sil, name="sil_uye"),
    path("uye/profil/<int:id>", uye_views.profil, name="profil_uye"),

    # Kort
    path("kort/index", kort_views.index_kort, name="index_kort"),
    path("kort/kaydet", kort_views.kaydet_kort, name="kaydet_kort"),
    path("kort/detay/<int:id>", kort_views.detay_kort, name="detay_kort"),
    path("kort/guncelle/<int:id>", kort_views.kaydet_kort, name="guncelle_kort"),
    path("kort/sil/<int:id>", kort_views.sil_kort, name="sil_kort"),

    # Antrenor
    path("antrenor/index", antrenor_views.index, name="index_antrenor"),
    path("antrenor/kaydet", antrenor_views.kaydet, name="kaydet_antrenor"),
    path("antrenor/profil/<int:id>", antrenor_views.profil, name="profil_antrenor"),
    path("antrenor/guncelle/<int:id>", antrenor_views.kaydet, name="guncelle_antrenor"),
    path("antrenor/sil/<int:id>", antrenor_views.sil, name="sil_antrenor"),

    # Grup
    path("grup/index", grup_views.index_grup, name="index_grup"),
    path("grup/kaydet", grup_views.kaydet_grup, name="kaydet_grup"),
    path("grup/detay/<int:id>", grup_views.detay_grup, name="detay_grup"),
    path("grup/guncelle/<int:id>", grup_views.kaydet_grup, name="guncelle_grup"),
    path("grup/sil/<int:id>", grup_views.sil_grup, name="sil_grup"),
    path("grup/sil", grup_views.sil_grup_uyesi, name="sil_grup_uyesi"),

    # Rezervasyon
    path("rezervasyon/index", rezervasyon_views.index, name="index_rezervasyon"),
    path("rezervasyon/kaydet", rezervasyon_views.kaydet, name="kaydet_rezervasyon"),
    path("rezervasyon/detay/<int:id>", rezervasyon_views.detay, name="detay_rezervasyon"),
    path("rezervasyon/guncelle/<int:id>", rezervasyon_views.kaydet, name="guncelle_rezervasyon"),
    path("rezervasyon/sil/<int:id>", rezervasyon_views.sil, name="sil_rezervasyon"),
    path("rezervasyon/bekleyen-musteri", rezervasyon_views.bekleyen_musteri_getir_ajax,
         name="bekleyen_musteri_getir_ajax"),

    # Telafi Ders
    path("telafi-ders/index", telafi_ders_views.index, name="index_telafi_ders"),
    path("telafi-ders/kaydet/<int:etkinlik_id>", telafi_ders_views.kaydet, name="kaydet_telafi_ders"),
    # path("telafi-ders/detay/<int:id>", telafi_ders_views.detay, name="detay_telafi_ders"),
    path("telafi-ders/guncelle/<int:id>", telafi_ders_views.guncelle, name="guncelle_telafi_ders"),
    path("telafi-ders/sil/<int:id>", telafi_ders_views.sil, name="sil_telafi_ders"),
    path("telafi-ders/kaydet-yapilan-telafi-ders/<int:telafi_id>", telafi_ders_views.kaydet_yapilan_telafi_ders, name="kaydet_yapilan_telafi_ders"),

    # Abonelik
    path("abonelik/kaydet-abonelik/<int:uye_id>", abonelik_views.kaydet_abonelik, name="kaydet_abonelik"),
    path("abonelik/guncelle-abonelik/<int:id>", abonelik_views.guncelle_abonelik, name="guncelle_abonelik"),
    path("abonelik/sil-abonelik/<int:id>", abonelik_views.sil_abonelik, name="sil_abonelik"),

    # Muhasebe
    path("muhasebe/index", muhasebe_views.index, name="index_muhasebe"),
    path("muhasebe/kaydet-uye-odemesi", muhasebe_views.kaydet_uye_odemesi_ajax, name="kaydet_uye_odemesi_ajax"),
    path("muhasebe/getir-odeme-by-id", muhasebe_views.getir_odeme_by_id_ajax, name="getir_odeme_by_id_ajax"),
    path("muhasebe/kaydet-antrenor-odemesi", muhasebe_views.kaydet_antrenor_odemesi_ajax, name="kaydet_antrenor_odemesi_ajax"),
    path("muhasebe/sil-odeme/<int:id>", muhasebe_views.sil_odeme, name="sil_odeme"),

]
