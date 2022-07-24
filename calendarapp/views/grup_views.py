from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
