from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.commons import SaatlerModel, GunlerModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.models.concrete.uye import UyeModel, GrupModel, UyeGrupModel


@login_required
def dasboard(request):
    tum_etkinlik_sayisi = EtkinlikModel.objects.filter(baslangic_tarih_saat__year=datetime.now().year,iptal_mi=False,).count()
    kortlar = KortModel.objects.all()
    antrenorler = AntrenorModel.objects.all()
    bugun_kalan_etkinlik_sayisi = EtkinlikModel.objects.getir_bugun_devam_eden_etkinlikler().count()
    gelecek_etkinlikler = EtkinlikModel.objects.getir_gelecek_etkinlikler()
    aktif_uye_sayisi = UyeModel.objects.filter(aktif_mi=True).count()
    html = render_to_string('calendarapp/anasayfa/_etkinlik_listesi_tablosu.html',
                            {'etkinlikler': gelecek_etkinlikler}, request=request)
    context = {
        "tum_etkinlik_sayisi": tum_etkinlik_sayisi,
        "bugun_kalan_etkinlik_sayisi": bugun_kalan_etkinlik_sayisi,
        "gelecek_etkinlikler": html,
        "aktif_uye_sayisi": aktif_uye_sayisi,
        "kortlar": kortlar,
        "antrenorler": antrenorler,
    }
    return render(request,'calendarapp/anasayfa/dashboard.html', context)


@login_required
def etkinlik_listesi_tablosu_getir_ajax(request):
    kort_id = request.GET.get('kort')
    antrenor_id = request.GET.get('antrenor')
    baslangic_tarih = request.GET.get('baslangic_tarihi')
    bitis_tarih = request.GET.get('bitis_tarihi')
    etkinlikler = EtkinlikModel.objects.all().order_by("baslangic_tarih_saat")
    if kort_id:
        etkinlikler = etkinlikler.filter(kort_id=kort_id)
    if baslangic_tarih:
        etkinlikler = etkinlikler.filter(baslangic_tarih_saat__gte=baslangic_tarih)
    if bitis_tarih:
        etkinlikler = etkinlikler.filter(bitis_tarih_saat__lte=bitis_tarih)
    if antrenor_id:
        etkinlikler = etkinlikler.filter(antrenor_id=antrenor_id)
    html = render_to_string('calendarapp/anasayfa/_etkinlik_listesi_tablosu.html',
                            {'etkinlikler': etkinlikler})
    return JsonResponse(
        data={"status": "success", "messages": "İşlem başarılı", "html": html})


@login_required
def baslangic_metodu(request):
    try:
        saatler_yoksa_ekle()
        gunler_yoksa_ekle()
        ilk_kayitlari_ekle()
        messages.success(request, "Başarılı")
        return redirect("dashboard")
    except Exception as e:
        messages.error(request, "Hata oluştu" + e)
        return redirect("dashboard")


def saatler_yoksa_ekle():
    if SaatlerModel.objects.count() == 0:
        from datetime import datetime
        from datetime import timedelta
        baslangic_degeri = datetime(1970, 1, 1, 00, 00, 00)
        bitis_degeri = datetime(1970, 1, 1, 00, 30, 00)
        for i in range(0, 48):
            SaatlerModel.objects.create(adi=str(baslangic_degeri.time())[0:5] + " - " + str(bitis_degeri.time())[0:5],
                                        baslangic_degeri=baslangic_degeri, bitis_degeri=bitis_degeri)
            baslangic_degeri += timedelta(minutes=30)
            bitis_degeri += timedelta(minutes=30)


def gunler_yoksa_ekle():
    if GunlerModel.objects.count() == 0:
        GunlerModel.objects.create(adi="Pazartesi", haftanin_gunu=0, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Salı", haftanin_gunu=1, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Çarşamba", haftanin_gunu=2, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Perşembe", haftanin_gunu=3, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Cuma", haftanin_gunu=4, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Cumartesi", haftanin_gunu=5, hafta_ici_mi=False)
        GunlerModel.objects.create(adi="Pazar", haftanin_gunu=6, hafta_ici_mi=False)


def ilk_kayitlari_ekle():
    if UyeModel.objects.count() == 0:
        UyeModel.objects.create(id=1, adi="İlk Üye", soyadi="Kayit")
    if GrupModel.objects.count() == 0:
        GrupModel.objects.create(id=1, adi="İlk Grup", tekil_mi=True)
    if UyeGrupModel.objects.count() == 0:
        UyeGrupModel.objects.create(id=1, grup_id=1, uye_id=1)
    if KortModel.objects.count() == 0:
        KortModel.objects.create(id=1, adi="Kort 1")
    if AntrenorModel.objects.count() == 0:
        AntrenorModel.objects.create(id=1, adi="Antrenör 1")
    if EtkinlikModel.objects.count() == 0:
        EtkinlikModel.objects.create(id=1, grup_id=1,
                                     baslangic_tarih_saat=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                     bitis_tarih_saat=datetime.now().strftime("%Y-%m-%d %H:%M"), kort_id=1,
                                     antrenor_id=1)
    if RezervasyonModel.objects.count() == 0:
        RezervasyonModel.objects.create(id=1, uye_id=1)
