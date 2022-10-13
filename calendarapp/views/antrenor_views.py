from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.antrenor_forms import AntrenorKayitForm
from calendarapp.models.Enums import KatilimDurumuEnum
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel, EtkinlikKatilimModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = AntrenorModel.objects.all().order_by('id')
    return render(request, "calendarapp/antrenor/index.html", {"list": form})


@login_required
def kaydet(request, id=None):
    if request.method == 'POST':
        entity = AntrenorModel.objects.filter(pk=id).first()
        form = AntrenorKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_antrenor")
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/antrenor/kaydet.html", context={'form': form})
    form = AntrenorKayitForm(instance=AntrenorModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/antrenor/kaydet.html", context={'form': form})


@login_required
def profil(request, id):
    antrenor = AntrenorModel.objects.filter(pk=id).first()
    yapilacak_etkinlikler = EtkinlikModel.objects.filter(antrenor_id=antrenor.id, baslangic_tarih_saat__gt=datetime.now(
    )).order_by('baslangic_tarih_saat')
    yapilan_etkinlikler = EtkinlikModel.objects.filter(antrenor_id=antrenor.id, bitis_tarih_saat__lt=datetime.now(
    )).order_by('-baslangic_tarih_saat')
    iptal_etkinlik_katilim_idler = EtkinlikKatilimModel.objects.filter(
        etkinlik__antrenor_id=antrenor.id, katilim_durumu=KatilimDurumuEnum.İptal.value).values('etkinlik')
    iptal_etkinlikler = EtkinlikModel.objects.filter(id__in=iptal_etkinlik_katilim_idler)
    odemeler = ParaHareketiModel.objects.filter(antrenor_id=antrenor.id).order_by('-tarih')
    return render(request, "calendarapp/antrenor/profil.html",
                  {"antrenor": antrenor, "yapilacak_etkinlikler": yapilacak_etkinlikler,
                   "yapilan_etkinlikler": yapilan_etkinlikler, "iptal_etkinlikler": iptal_etkinlikler,
                   "odemeler": odemeler})


@login_required
def sil(request, id):
    AntrenorModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_antrenor")
