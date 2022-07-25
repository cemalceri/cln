from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from calendarapp.forms.rezervasyon_forms import RezervasyonKayitForm
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = RezervasyonModel.objects.all().order_by('-id')
    return render(request, "calendarapp/rezervasyon/index.html", {"list": form})


@login_required
def kaydet(request, id=None):
    if request.method == 'POST':
        entity = RezervasyonModel.objects.filter(pk=id).first()
        form = RezervasyonKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Üye kaydedildi.")
            return redirect("calendarapp:index_rezervasyon")
        else:
            messages.error(request, formErrorsToText(form.errors, RezervasyonModel))
            return render(request, "calendarapp/rezervasyon/kaydet.html", context={'form': form})
    form = RezervasyonKayitForm(instance=RezervasyonModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/rezervasyon/kaydet.html", context={'form': form})


@login_required
def detay(request, id):
    pass


@login_required
def sil(request, id):
    RezervasyonModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_rezervasyon")
