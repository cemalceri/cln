from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.abonelik_forms import UyeAbonelikKayitForm, PaketKayitForm
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, PaketModel
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.uye import UyeModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = PaketModel.objects.all().order_by('id')
    return render(request, "calendarapp/abonelik/index.html", {"list": form})


@login_required
def kaydet(request, id=None):
    paket = PaketModel.objects.filter(pk=id).first()
    if request.method == 'POST':
        form = PaketKayitForm(request.POST, instance=paket)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_paket")
        else:
            messages.error(request, formErrorsToText(form.errors, PaketModel))
            return render(request, "calendarapp/abonelik/kaydet.html", context={'form': form})
    form = PaketKayitForm(instance=paket)
    return render(request, "calendarapp/abonelik/kaydet.html", context={'form': form})


@login_required
def kaydet_uye_abonelik(request, uye_id):
    if request.method == 'POST':
        form = UyeAbonelikKayitForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:profil_uye", uye_id)
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})
    form = UyeAbonelikKayitForm(initial={'uye': UyeModel.objects.filter(pk=uye_id).first()})
    return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})


def guncelle_uye_abonelik(request, id):
    entity = UyeAbonelikModel.objects.filter(pk=id).first()
    if request.method == 'POST':
        form = UyeAbonelikKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:profil_uye", entity.uye.id)
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})
    form = UyeAbonelikKayitForm(instance=entity)
    return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})


@login_required
def detay(request, id):
    pass


@login_required
def sil_abonelik(request, id):
    abonelik = UyeAbonelikModel.objects.filter(pk=id).first()
    uye_id = abonelik.uye.id
    abonelik.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:profil_uye", uye_id)


@login_required
def sil(request, id):
    abonelik = PaketModel.objects.filter(pk=id).first()
    abonelik.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_paket")
