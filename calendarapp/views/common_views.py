from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.common_forms import OkulKayitForm
from calendarapp.models.concrete.commons import OkulModel
from calendarapp.utils import formErrorsToText


@login_required
def index_okul(request):
    form = OkulModel.objects.all().order_by('-id')
    return render(request, "calendarapp/common/okul/index.html", {"list": form})


@login_required
def kaydet_okul(request, id=None):
    if request.method == 'POST':
        entity = OkulModel.objects.filter(pk=id).first()
        form = OkulKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_okul")
        else:
            messages.error(request, formErrorsToText(form.errors, OkulModel))
            return render(request, "calendarapp/common/okul/kaydet.html", context={'form': form})
    form = OkulKayitForm(instance=OkulModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/common/okul/kaydet.html", context={'form': form})


@login_required
def sil_okul(request, id):
    OkulModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_kort")
