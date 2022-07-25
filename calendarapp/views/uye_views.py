from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.uye_forms import UyeKayitForm
from calendarapp.models.concrete.uye import UyeModel
from calendarapp.utils import formErrorsToText


@login_required
def index_uye(request):
    form = UyeModel.objects.all().order_by('-id')
    return render(request, "calendarapp/uye/index.html", {"uye_list": form})


@login_required
def kaydet_uye(request, id=None):
    if request.method == 'POST':
        entity = UyeModel.objects.filter(pk=id).first()
        form = UyeKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Üye kaydedildi.")
            return redirect("calendarapp:index_uye")
        else:
            messages.error(request, formErrorsToText(form.errors, UyeModel))
            return render(request, "calendarapp/uye/kaydet.html", context={'form': form})
    form = UyeKayitForm(instance=UyeModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/uye/kaydet.html", context={'form': form})


@login_required
def detay_uye(request, id):
    pass


@login_required
def sil_uye(request, id):
    UyeModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_uye")
