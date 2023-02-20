from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.uye_forms import UyeKayitForm, GencUyeKayitForm
from calendarapp.models.Enums import KatilimDurumuEnum, UyeTipiEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, UyePaketModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel
from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = UyeModel.objects.all().order_by('-id')
    return render(request, "calendarapp/uye/index.html", {"uye_list": form})


@login_required
def kaydet(request, id=None, uye_tipi=None):
    if request.method == 'POST':
        entity = UyeModel.objects.filter(pk=id).first()
        uye_tipi = request.POST.get("uye_tipi")
        form = UyeKayitForm(request.POST,
                            instance=entity) if uye_tipi == UyeTipiEnum.Yetişkin.value else GencUyeKayitForm(
            request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            form.save_m2m()
            messages.success(request, "Üye kaydedildi.")
            return redirect("calendarapp:index_uye")
        else:
            messages.error(request, formErrorsToText(form.errors, UyeModel))
            return render(request, "calendarapp/uye/kaydet.html", context={'form': form})
    else:
        duzenleme_mi = False
        if id is not None:
            uye = UyeModel.objects.filter(pk=id).first()
            uye_tipi = uye.uye_tipi
            duzenleme_mi = True
            form = UyeKayitForm(instance=uye) if uye_tipi == UyeTipiEnum.Yetişkin.value else GencUyeKayitForm(
                instance=uye)
        elif uye_tipi is not None:
            form = UyeKayitForm() if uye_tipi == UyeTipiEnum.Yetişkin.value else GencUyeKayitForm()
        else:
            form = None
    return render(request, "calendarapp/uye/kaydet.html",
                  context={'form': form, 'uye_tipi': uye_tipi, 'duzenleme_mi': duzenleme_mi})


@login_required
def sil(request, id):
    UyeModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_uye")


@login_required
def profil(request, id):
    uye = UyeModel.objects.filter(pk=id).first()
    abonelikler = UyeAbonelikModel.objects.filter(uye_id=id)
    paketler = UyePaketModel.objects.filter(uye_id=id)
    gruplar = UyeGrupModel.objects.filter(uye_id=id).values_list('grup_id', flat=True)
    yapilacak_etkinlikler = EtkinlikModel.objects.filter(grup_id__in=gruplar, baslangic_tarih_saat__gt=datetime.now(
    )).order_by('baslangic_tarih_saat')
    yapilan_etkinlikler = EtkinlikModel.objects.filter(grup_id__in=gruplar, bitis_tarih_saat__lt=datetime.now(
    )).order_by('-baslangic_tarih_saat')
    iptal_etkinlikler = EtkinlikModel.objects.filter(grup_id__in=gruplar, iptal_mi=True).order_by(
        '-baslangic_tarih_saat')
    return render(request, "calendarapp/uye/profil.html",
                  {"uye": uye, "abonelikler": abonelikler, "paketler": paketler,
                   "yapilacak_etkinlikler": yapilacak_etkinlikler, "yapilan_etkinlikler": yapilan_etkinlikler,
                   "iptal_etkinlikler": iptal_etkinlikler})


