from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.abonelik_forms import UyePaketKayitForm
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, UyePaketModel
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.uye import UyeModel
from calendarapp.utils import formErrorsToText


@login_required
def index_uye_paket(request):
    form = UyePaketModel.objects.all().order_by('id')
    return render(request, "calendarapp/abonelik/index.html", {"list": form})


# @login_required
# def kaydet(request, id=None):
#     paket = PaketModel.objects.filter(pk=id).first()
#     if request.method == 'POST':
#         form = PaketKayitForm(request.POST, instance=paket)
#         if form.is_valid():
#             entity = form.save(commit=False)
#             entity.user = request.user
#             entity.save()
#             messages.success(request, "Kaydedildi.")
#             return redirect("calendarapp:index_paket")
#         else:
#             messages.error(request, formErrorsToText(form.errors, PaketModel))
#             return render(request, "calendarapp/abonelik/kaydet.html", context={'form': form})
#     form = PaketKayitForm(instance=paket)
#     return render(request, "calendarapp/abonelik/kaydet.html", context={'form': form})


@login_required
def kaydet_uye_paket(request, uye_id):
    if request.method == 'POST':
        form = UyePaketKayitForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:profil_uye", uye_id)
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/abonelik/uye_paket_kaydet.html", context={'form': form})
    form = UyePaketKayitForm(initial={'uye': UyeModel.objects.filter(pk=uye_id).first()})
    return render(request, "calendarapp/abonelik/uye_paket_kaydet.html", context={'form': form})


def guncelle_uye_paket(request, id):
    entity = UyePaketModel.objects.filter(pk=id).first()
    if request.method == 'POST':
        form = UyePaketKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:profil_uye", entity.uye.id)
        else:
            messages.error(request, formErrorsToText(form.errors, AntrenorModel))
            return render(request, "calendarapp/abonelik/uye_paket_kaydet.html", context={'form': form})
    form = UyePaketKayitForm(instance=entity)
    return render(request, "calendarapp/abonelik/uye_paket_kaydet.html", context={'form': form})


# @login_required
# def detay(request, id):
#     uye_paket_listesi = UyeAbonelikModel.objects.filter(paket_id=id)
#     paket = PaketModel.objects.filter(pk=id).first()
#     return render(request, "calendarapp/abonelik/detay.html", {"uye_paket_listesi": uye_paket_listesi, "paket": paket})


@login_required
def sil_uye_paket(request, id):
    abonelik = UyePaketModel.objects.filter(pk=id).first()
    uye_id = abonelik.uye.id
    abonelik.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:profil_uye", uye_id)

#
# @login_required
# def sil(request, id):
#     abonelik = PaketModel.objects.filter(pk=id).first()
#     abonelik.delete()
#     messages.success(request, "Kayıt Silindi.")
#     return redirect("calendarapp:index_paket")
