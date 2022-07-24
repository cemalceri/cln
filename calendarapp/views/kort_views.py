from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.kort_forms import KortKayitForm
from calendarapp.models.concrete.kort import KortModel
from calendarapp.utils import formErrorsToText


@login_required
def index_kort(request):
    form = KortModel.objects.all().order_by('-id')
    return render(request, "calendarapp/kort/index.html", {"list": form})


@login_required
def kaydet_kort(request, id=None):
    if request.method == 'POST':
        entity = KortModel.objects.filter(pk=id).first()
        form = KortKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_kort")
        else:
            messages.error(request, formErrorsToText(form.errors, KortModel))
            return render(request, "calendarapp/kort/kaydet.html", context={'form': form})
    form = KortKayitForm(instance=KortModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/kort/kaydet.html", context={'form': form})


@login_required
def detay_kort(request, id):
    pass


@login_required
def sil_kort(request, id):
    KortModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_kort")
