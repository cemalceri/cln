from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.abonelik_forms import AbonelikKayitForm
from calendarapp.models.concrete.abonelik import AbonelikModel
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.uye import UyeModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = AntrenorModel.objects.all().order_by('id')
    return render(request, "calendarapp/antrenor/index.html", {"list": form})


@login_required
def kaydet_abonelik(request, uye_id):
    print("uye_id: ", uye_id)
    if request.method == 'POST':
        form = AbonelikKayitForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:profil_uye", uye_id)
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})
    form = AbonelikKayitForm(initial={'uye': UyeModel.objects.filter(pk=uye_id).first()})
    return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})


def guncelle_abonelik(request, id):
    entity = AbonelikModel.objects.filter(pk=id).first()
    if request.method == 'POST':
        form = AbonelikKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:profil_uye", entity.uye.id)
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})
    form = AbonelikKayitForm(instance=entity)
    return render(request, "calendarapp/abonelik/uye_abonelik_kaydet.html", context={'form': form})


@login_required
def detay(request, id):
    pass


@login_required
def sil_abonelik(request, id):
    abonelik = AbonelikModel.objects.filter(pk=id).first()
    uye_id = abonelik.uye.id
    abonelik.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:profil_uye", uye_id)
