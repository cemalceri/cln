from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from calendarapp.models.concrete.etkinlik import EtkinlikModel


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        tum_etkinlik_sayisi = EtkinlikModel.objects.filter(is_active=True, is_deleted=False).count()
        bugun_kalan_etkinlik_sayisi = EtkinlikModel.objects.getir_bugun_devam_eden_etkinlikler().count()
        gelecek_etkinlikler = EtkinlikModel.objects.getir_gelecek_etkinlikler()

        context = {
            "tum_etkinlik_sayisi": tum_etkinlik_sayisi,
            "bugun_kalan_etkinlik_sayisi": bugun_kalan_etkinlik_sayisi,
            "gelecek_etkinlikler": gelecek_etkinlikler,
        }
        return render(request, self.template_name, context)


@login_required
def baslangic_metodu(request):
    try:
        saatler_yoksa_ekle()
        gunler_yoksa_ekle()
        messages.success(request, "Başarılı")
        return redirect("dashboard")
    except Exception as e:
        messages.error(request, "Hata oluştu" + e)
        return redirect("dashboard")


def saatler_yoksa_ekle():
    from calendarapp.models.Enums import SaatlerModel
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
    from calendarapp.models.Enums import GunlerModel
    if GunlerModel.objects.count() == 0:
        GunlerModel.objects.create(adi="Pazartesi", haftanin_gunu=0, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Salı", haftanin_gunu=1, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Çarşamba", haftanin_gunu=2, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Perşembe", haftanin_gunu=3, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Cuma", haftanin_gunu=4, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Cumartesi", haftanin_gunu=5, hafta_ici_mi=False)
        GunlerModel.objects.create(adi="Pazar", haftanin_gunu=6, hafta_ici_mi=False)
