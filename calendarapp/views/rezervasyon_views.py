from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from calendarapp.forms.rezervasyon_forms import RezervasyonKayitForm
from calendarapp.models.Enums import GunlerModel, SaatlerModel
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
            form.save_m2m()
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


@login_required
def bekleyen_musteri_getir_ajax(request):
    tarih_saat = request.GET.get("tarih_saat")
    gunun_saati = datetime.strptime(tarih_saat, "%Y-%m-%dT%H:%M:%S").time()
    haftanini_gunu = datetime.strptime(tarih_saat, "%Y-%m-%dT%H:%M:%S").weekday()
    gun = GunlerModel.objects.filter(haftanin_gunu=haftanini_gunu).first()
    saat = SaatlerModel.objects.filter(baslangic_degeri=gunun_saati).first()
    rezervasyonlar = RezervasyonModel.objects.filter(
        Q(gunler=gun, saatler=saat) | Q(gunler__isnull=True, saatler__isnull=True))
    list = []
    for rezervasyon in rezervasyonlar:
        list.append({"id": rezervasyon.id, "adi": rezervasyon.adi, "aciklama": rezervasyon.aciklama})
    print(list)
    return JsonResponse(data={"data": list, "durum": "ok", "mesaj": "Başarılı"}, safe=False)
