from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.antrenor_forms import AntrenorKayitForm
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.utils import formErrorsToText


@login_required
def index_antrenor(request):
    form = AntrenorModel.objects.all().order_by('id')
    return render(request, "calendarapp/antrenor/index.html", {"list": form})


@login_required
def kaydet_antrenor(request, id=None):
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
def detay_antrenor(request, id):
    pass


@login_required
def sil_antrenor(request, id):
    AntrenorModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_antrenor")
