from django.urls import path

from .views import etkinlik_views, rezervasyon_views, telafi_ders_views, abonelik_views
from .views import uye_views
from .views import kort_views
from .views import antrenor_views
from .views import grup_views
from .views import muhasebe_views
from .views import haftalik_plan_views

app_name = "calendarapp"

urlpatterns = [
    # Takvim ve Etkinlikler
    path("takvim/", etkinlik_views.takvim_getir, name="takvim_getir"),
    path("takvim/<int:kort_id>", etkinlik_views.takvim_getir, name="takvim_getir_by_kort_id"),
    path("etkinlik", etkinlik_views.index, name="index_etkinlik"),
    path("gunun_etkinlikleri", etkinlik_views.gunun_etkinlikleri_ajax, name="gunun_etkinlikleri_ajax"),
    path("etkinlik/index/<str:tarih>", etkinlik_views.index_getir_by_tarih, name="index_getir_by_tarih"),

    # Haftalık Plan
    path("haftalik-plan/", haftalik_plan_views.haftalik_plan_getir, name="haftalik_plan_getir"),
    path("haftalik-plan/<int:kort_id>", haftalik_plan_views.haftalik_plan_getir, name="haftalik_plan_getir_by_kort_id"),
    path("haftalik-plan/kaydet", haftalik_plan_views.kaydet_haftalik_plan_ajax, name="kaydet_haftalik_plan_ajax"),
    path("haftalik-plan/detay", haftalik_plan_views.getir_haftalik_plan_bilgisi_ajax, name="getir_haftalik_plan_bilgisi_ajax"),
    path("haftalik-plan/tasi", haftalik_plan_views.haftalik_plan_saat_bilgisi_guncelle_ajax, name="haftalik_plan_saat_bilgisi_guncelle_ajax"),
    path("plan/sil", haftalik_plan_views.sil_haftalik_plan_ajax, name="sil_haftalik_plan_ajax"),
    # path("plan/haftalik-plani-takvime-ekle", haftalik_plan_views.haftalik_plani_takvime_ekle_ajax, name="haftalik_plani_takvime_ekle_ajax"),

    # Etkinlik
    path("etkinlik/detay", etkinlik_views.getir_etkinlik_bilgisi_ajax, name="getir_etkinlik_by_id"),
    path("etkinlik/sil", etkinlik_views.sil_etkinlik_ajax, name="sil_etkinlik_by_ajax"),
    path("etkinlik/sil/<int:id>", etkinlik_views.sil_etkinlik, name="sil_etkinlik_by_id"),
    path("etkinlik/kaydet", etkinlik_views.kaydet_etkinlik_ajax, name="kaydet_etkinlik_ajax"),
    path("etkinlik/tasi", etkinlik_views.saat_guncelle_etkinlik_ajax, name="saat_guncelle_etkinlik_ajax"),
    path("etkinlik/tamamlandi", etkinlik_views.etkinlik_tamamlandi_ajax, name="etkinlik_tamamlandi_ajax"),
    path("etkinlik/tamamlandi-iptal", etkinlik_views.etkinlik_tamamlandi_iptal_ajax, name="etkinlik_tamamlandi_iptal_ajax"),
    path("etkinlik/modal-detay-getir", etkinlik_views.etkinlik_detay_getir_ajax, name="etkinlik_detay_getir_ajax"),
    path("etkinlik/modal-etkinlik-kaydet", etkinlik_views.etkinlik_kaydet_modal_ajax, name="etkinlik_kaydet_modal_ajax"),
    path("etkinlik/modal-etkinlik-getir", etkinlik_views.etkinlik_getir_modal_ajax, name="etkinlik_getir_modal_ajax"),

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
    path("grup/guncelle/<int:id>", grup_views.kaydet_grup, name="guncelle_grup"),
    path("grup/guncelle-grup-adi", grup_views.guncelle_grup_adi, name="guncelle_grup_adi"),
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
    path("rezervasyon/bekleyen-musteri-modal", rezervasyon_views.bekleyen_musteri_modal_getir_ajax,
         name="bekleyen_musteri_modal_getir_ajax"),

    # Telafi Ders
    path("telafi-ders/index", telafi_ders_views.index, name="index_telafi_ders"),
    path("telafi-ders/kaydet/<int:etkinlik_id>", telafi_ders_views.kaydet, name="kaydet_telafi_ders"),
    # path("telafi-ders/detay/<int:id>", telafi_ders_views.detay, name="detay_telafi_ders"),
    path("telafi-ders/guncelle/<int:id>", telafi_ders_views.guncelle, name="guncelle_telafi_ders"),
    path("telafi-ders/sil/<int:id>", telafi_ders_views.sil, name="sil_telafi_ders"),
    path("telafi-ders/kaydet-yapilan-telafi-ders/<int:telafi_id>", telafi_ders_views.kaydet_yapilan_telafi_ders,
         name="kaydet_yapilan_telafi_ders"),

    # Abonelik
    path("abonelik/index", abonelik_views.index_uye_paket, name="index_uye_paket"),
    # path("abonelik/kaydet", abonelik_views.kaydet, name="kaydet_paket"),
    # path("abonelik/guncelle/<int:id>", abonelik_views.kaydet, name="guncelle_paket"),
    # path("abonelik/sil/<int:id>", abonelik_views.sil, name="sil_paket"),
    # path("abonelik/detay/<int:id>", abonelik_views.detay, name="detay_paket"),
    path("abonelik/kaydet-uye-paket/<int:uye_id>", abonelik_views.kaydet_uye_paket, name="kaydet_uye_paket"),
    path("abonelik/guncelle-uye_paket/<int:id>", abonelik_views.guncelle_uye_paket, name="guncelle_uye_paket"),
    path("abonelik/sil_uye_paket/<int:id>", abonelik_views.sil_uye_paket, name="sil_uye_paket"),

    # Muhasebe
    path("muhasebe/index", muhasebe_views.index, name="index_muhasebe"),
    path("muhasebe/kaydet-uye-odemesi", muhasebe_views.kaydet_uye_odemesi_ajax, name="kaydet_uye_odemesi_ajax"),
    path("muhasebe/getir-odeme-by-id", muhasebe_views.getir_odeme_by_id_ajax, name="getir_odeme_by_id_ajax"),
    path("muhasebe/kaydet-antrenor-odemesi", muhasebe_views.kaydet_antrenor_odemesi_ajax,
         name="kaydet_antrenor_odemesi_ajax"),
    path("muhasebe/sil-odeme/<int:id>", muhasebe_views.sil_odeme, name="sil_odeme"),

]
