from django.urls import path

from .views import etkinlik_views as ev, rezervasyon_views as rv, telafi_ders_views, abonelik_views
from .views import uye_views
from .views import kort_views
from .views import antrenor_views
from .views import grup_views
from .views import muhasebe_views
from .views.eski import haftalik_plan_views
from .views import sabit_plan_views as hfsp_views

app_name = "calendarapp"

urlpatterns = [
    # Takvim ve Etkinlikler -> Eski sayfaların
    path("takvim/", ev.takvim_getir, name="takvim_getir"),
    path("takvim/<int:kort_id>", ev.takvim_getir, name="takvim_getir_by_kort_id"),
    path("gunun_etkinlikleri", ev.gunun_etkinlikleri_ajax, name="gunun_etkinlikleri_ajax"),
    # path("etkinlik/index/<str:tarih>", ev.index_getir_by_tarih, name="index_getir_by_tarih"),

    # Haftalık Plan -> Eski sayfaların
    path("haftalik-plan/", haftalik_plan_views.haftalik_plan_getir, name="haftalik_plan_getir"),
    path("haftalik-plan/<int:kort_id>", haftalik_plan_views.haftalik_plan_getir, name="haftalik_plan_getir_by_kort_id"),
    path("haftalik-plan/kaydet", haftalik_plan_views.kaydet_haftalik_plan_ajax, name="kaydet_haftalik_plan_ajax"),
    path("haftalik-plan/detay", haftalik_plan_views.getir_haftalik_plan_bilgisi_ajax,
         name="getir_haftalik_plan_bilgisi_ajax"),
    path("haftalik-plan/tasi", haftalik_plan_views.haftalik_plan_saat_bilgisi_guncelle_ajax,
         name="haftalik_plan_saat_bilgisi_guncelle_ajax"),
    path("plan/sil", haftalik_plan_views.sil_haftalik_plan_ajax, name="sil_haftalik_plan_ajax"),

    # Haftalık Sabit Plan
    path("sabit-plan", hfsp_views.index, name="index_sabit_plan"),
    path("sabit-plan-ajax", hfsp_views.gunun_planlari_ajax, name="sabit_plan_gunun_etkinlikleri_ajax"),
    path("sabit-plan/kaydet", hfsp_views.kaydet_ajax, name="sabit_plan_kaydet_ajax"),
    path("sabit-plan/kaydet-modal", hfsp_views.kaydet_modal_ajax, name="sabit_plan_kaydet_modal_getir_ajax"),
    path("sabit-plan/detay_modal", hfsp_views.detay_modal_ajax, name="sabit_plan_detay_modal_getir_ajax"),
    path("sabit-plan/sil", hfsp_views.sil_ajax, name="sabit_plan_sil_ajax"),
    path("sabit-plan/duzenle-modal", hfsp_views.duzenle_modal_ajax, name="sabit_plan_duzenle_modal_getir_ajax"),

    # Etkinlik
    path("etkinlik", ev.index, name="index_etkinlik"),
    path("etkinlik/index/<str:tarih>", ev.index_getir_by_tarih, name="index_etkinlik_by_tarih"),
    path("etkinlik/detay", ev.getir_etkinlik_bilgisi_ajax, name="getir_etkinlik_by_id_ajax"),
    path("etkinlik/sil", ev.sil_etkinlik_ajax, name="sil_etkinlik_by_ajax"),
    path("etkinlik/sil/<int:id>", ev.sil_etkinlik, name="sil_etkinlik_by_id"),
    path("etkinlik/kaydet", ev.kaydet_etkinlik_ajax, name="kaydet_etkinlik_ajax"),
    path("etkinlik/tasi", ev.saat_guncelle_etkinlik_ajax, name="saat_guncelle_etkinlik_ajax"),
    path("etkinlik/tamamlandi", ev.etkinlik_tamamlandi_ajax, name="etkinlik_tamamlandi_ajax"),
    path("etkinlik/tamamlandi-iptal", ev.tamamlandi_iptal_ajax, name="etkinlik_tamamlandi_iptal_ajax"),
    path("etkinlik/datay-modal", ev.detay_modal_ajax, name="etkinlik_detay_modal_getir_ajax"),
    path("etkinlik/kaydet-modal", ev.kaydet_modal_ajax, name="etkinlik_kaydet_modal_getir_ajax"),
    path("etkinlik/duzenle-modal", ev.duzenle_modal_ajax, name="etkinlik_duzenle_modal_getir_ajax"),
    path("etkinlik/haftayi-olustur", ev.haftayi_sabit_plandan_olustur_ajax, name="haftanin_etkinliklerini_sabit_plandan_olustur_ajax"),
    path("etkinlik/haftayi-sil", ev.haftanin_etkinliklerini_sil_ajax, name="haftanin_etkinliklerini_sil_ajax"),

    # Uye
    path("uye/index", uye_views.index, name="index_uye"),
    path("uye/kaydet-post", uye_views.kaydet, name="kaydet_post"),
    path("uye/kaydet/<int:uye_tipi>", uye_views.kaydet, name="kaydet_uye"),
    path("uye/guncelle/<int:id>", uye_views.kaydet, name="guncelle_uye"),
    path("uye/sil/<int:id>", uye_views.sil, name="sil_uye"),
    path("uye/profil/<int:id>", uye_views.profil, name="profil_uye"),
    path("uye/muhasebe/<int:uye_id>", uye_views.muhasebe_uye, name="muhasebe_uye"),
    path("uye/muhasebe-detay/", uye_views.muhasebe_detay_modal_getir_ajax, name="uye_muhasebe_detay_modal_getir_ajax"),
    path("uye/muhasebe-odeme-girisi/", uye_views.muhasebe_odeme_modal_getir_ajax, name="uye_muhasebe_odeme_modal_getir_ajax"),
    path("uye/kaydet-uye-odemesi/", uye_views.kaydet_uye_odemesi_ajax, name="kaydet_uye_odemesi_ajax"),

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
    path("grup/ara", grup_views.ara_ajax, name="grup_ara_ajax"),

    # Rezervasyon
    path("rezervasyon/index", rv.index, name="index_rezervasyon"),
    path("rezervasyon/kaydet", rv.kaydet, name="kaydet_rezervasyon"),
    path("rezervasyon/detay/<int:id>", rv.detay, name="detay_rezervasyon"),
    path("rezervasyon/guncelle/<int:id>", rv.kaydet, name="guncelle_rezervasyon"),
    path("rezervasyon/sil/<int:id>", rv.sil, name="sil_rezervasyon"),
    path("rezervasyon/bekleyen-musteri", rv.bekleyen_musteri_getir_ajax, name="bekleyen_musteri_getir_ajax"),
    path("rezervasyon/bekleyen-musteri-modal", rv.bekleyen_musteri_modal_getir_ajax,
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
    path("muhasebe/getir-odeme-by-id", muhasebe_views.getir_odeme_by_id_ajax, name="getir_odeme_by_id_ajax"),
    path("muhasebe/kaydet-antrenor-odemesi", muhasebe_views.kaydet_antrenor_odemesi_ajax,
         name="kaydet_antrenor_odemesi_ajax"),
    path("muhasebe/sil-odeme/<int:id>", muhasebe_views.sil_odeme, name="sil_odeme"),

]
