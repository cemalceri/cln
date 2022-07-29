from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.antrenor_forms import AntrenorKayitForm
from calendarapp.forms.telafi_ders_forms import TelafiDersKayitForm
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = AntrenorModel.objects.all().order_by('id')
    return render(request, "calendarapp/antrenor/index.html", {"list": form})


@login_required
def kaydet(request, etkinlik_id=None):
    if request.method == 'POST':
        entity = AntrenorModel.objects.filter(pk=id).first()
        form = AntrenorKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_telafi_ders")
        else:
            messages.error(request, formErrorsToText(form.errors, TelafiDersModel))
            return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form})
    form = TelafiDersKayitForm(data={"etkinlik_id": etkinlik_id})
    return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form})


@login_required
def detay(request, id):
    pass


@login_required
def sil(request, id):
    AntrenorModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_antrenor")
