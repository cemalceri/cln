from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from calendarapp.forms.uye_forms import UyeGrupKayitForm
from calendarapp.models.concrete.uye import UyeGrupModel
from calendarapp.utils import formErrorsToText


@login_required
def index_grup(request):
    form = UyeGrupModel.objects.all().order_by('-id')
    return render(request, "calendarapp/grup/index.html", {"list": form})


@login_required
def kaydet_grup(request, id=None):
    if request.method == 'POST':
        entity = UyeGrupModel.objects.filter(pk=id).first()
        form = UyeGrupKayitForm(request.POST, instance=entity)
        if form.is_valid():
            result = grup_kaydi_hata_var_mi(form)
            if result:
                messages.error(request, result)
                return render(request, "calendarapp/grup/kaydet.html", context={'form': form})
                # return redirect("calendarapp:index_grup")
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_grup")
        else:
            messages.error(request, formErrorsToText(form.errors, UyeGrupModel))
            return render(request, "calendarapp/grup/kaydet.html", context={'form': form})
    form = UyeGrupKayitForm(instance=UyeGrupModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/grup/kaydet.html", context={'form': form})


@login_required
def detay_grup(request, id):
    pass


@login_required
def sil_grup(request, id):
    UyeGrupModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_grup")


def grup_kaydi_hata_var_mi(form):
    mesaj = None
    if ayni_uye_iki_defa_secilmis_mi(form):
        mesaj = "Aynı üye iki defa seçilemez."
    elif ayni_grup_kayitli_mi(form):
        mesaj = "Bu grup daha önce kayıt edilmiş."
    return mesaj


def ayni_grup_kayitli_mi(form):
    uye1 = form.cleaned_data["uye1"]
    uye2 = form.cleaned_data["uye2"]
    uye3 = form.cleaned_data["uye3"]
    uye4 = form.cleaned_data["uye4"]
    return UyeGrupModel.objects.filter(
        Q(uye1=uye1) | Q(uye2=uye1) | Q(uye3=uye1) | Q(uye4=uye1)).filter(
        Q(uye1=uye2) | Q(uye2=uye2) | Q(uye3=uye2) | Q(uye4=uye2)).filter(
        Q(uye1=uye3) | Q(uye2=uye3) | Q(uye3=uye3) | Q(uye4=uye3)).filter(
        Q(uye1=uye4) | Q(uye2=uye4) | Q(uye3=uye4) | Q(uye4=uye4)).exists()


def ayni_uye_iki_defa_secilmis_mi(form):
    uye1 = form.data["uye1"]
    uye2 = form.data["uye2"]
    uye3 = form.data["uye3"]
    uye4 = form.data["uye4"]
    if uye1 and (uye1 == uye2 or uye1 == uye3 or uye1 == uye4):
        return True
    if uye2 and (uye2 == uye3 or uye2 == uye4):
        return True
    if uye3 and (uye3 == uye4):
        return True
    return False
