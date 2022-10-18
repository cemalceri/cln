from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from calendarapp.forms.antrenor_forms import AntrenorKayitForm
from calendarapp.forms.telafi_ders_forms import TelafiDersKayitForm, TelafiDersGetirForm, TelafiDersGuncelleForm, \
    YapilanTelafiDersForm
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel
from calendarapp.models.concrete.uye import UyeGrupModel, UyeModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = TelafiDersModel.objects.all().order_by('id')
    return render(request, "calendarapp/telafi_ders/index.html", {"list": form})


@login_required
def kaydet(request, etkinlik_id):
    if request.method == 'POST':
        form = TelafiDersKayitForm(request.POST)
        if form.is_valid():
            if telafi_ders_kaydi_hata_var_mi(request, form, etkinlik_id):
                return render(request, "calendarapp/telafi_ders/kaydet.html",
                              context={'form': form, 'etkinlik_id': etkinlik_id})
            entity = form.save(commit=False)
            entity.telafi_etkinlik_id = etkinlik_id
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_telafi_ders")
        else:
            messages.error(request, formErrorsToText(form.errors, TelafiDersModel))
            return render(request, "calendarapp/telafi_ders/kaydet.html",
                          context={'form': form, 'etkinlik_id': etkinlik_id})
    etkinlik = EtkinlikModel.objects.filter(id=etkinlik_id).first()
    uye_idler = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id).values_list("uye_id", flat=True)
    etkinlik_uyeleri = UyeModel.objects.filter(id__in=uye_idler)
    form = TelafiDersKayitForm(
        initial={"uye": etkinlik_uyeleri})
    return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form, 'etkinlik_id': etkinlik_id})


@login_required
def guncelle(request, id):
    if request.method == 'POST':
        entity = TelafiDersModel.objects.filter(pk=id).first()
        form = TelafiDersGuncelleForm(request.POST, instance=entity)
        if form.is_valid():
            if telafi_ders_kaydi_hata_var_mi(request, form, entity.telafi_etkinlik_id, id):
                return render(request, "calendarapp/telafi_ders/kaydet.html",
                              context={'form': form, 'etkinlik_id': entity.telafi_etkinlik_id})
            entity = form.save(commit=False)
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_telafi_ders")
        else:
            messages.error(request, formErrorsToText(form.errors, TelafiDersModel))
            return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form, 'telafi_ders_id': id})
    form = TelafiDersGuncelleForm(instance=TelafiDersModel.objects.get(pk=id))
    return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form, 'telafi_ders_id': id})


@login_required
def detay(request, id):
    pass


@login_required
def sil(request, id):
    TelafiDersModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_telafi_ders")


def telafi_ders_kaydi_hata_var_mi(request, form, etkinlik_id, telafi_ders_id=None):
    if TelafiDersModel.objects.filter(uye_id=form.cleaned_data["uye"], telafi_etkinlik_id=etkinlik_id).exclude(
            pk=telafi_ders_id).exists():
        messages.error(request, "Bu üyenin telafi dersi zaten kayıtlı.")
        return True


@login_required
def kaydet_yapilan_telafi_ders(request, telafi_id):
    if request.method == 'POST':
        print("POST")
        form = YapilanTelafiDersForm(request.POST, instance=TelafiDersModel.objects.get(pk=telafi_id))
        print(form)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_telafi_ders")
        else:
            messages.error(request, formErrorsToText(form.errors, TelafiDersModel))
            return render(request, "calendarapp/telafi_ders/kaydet_yapilan_telafi.html",
                          {'form': form, 'telafi_id': telafi_id})
    telafi = TelafiDersModel.objects.filter(id=telafi_id).first()
    form = YapilanTelafiDersForm(instance=telafi)
    return render(request, "calendarapp/telafi_ders/kaydet_yapilan_telafi.html", {'form': form, 'telafi_id': telafi_id})
