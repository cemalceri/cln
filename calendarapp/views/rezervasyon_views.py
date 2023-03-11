from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from calendarapp.forms.rezervasyon_forms import RezervasyonKayitForm
from calendarapp.models.concrete.commons import GunlerModel, SaatlerModel
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
    rezervasyonlar = bekleyen_musteri_getir(request.GET.get("tarih_saat"))
    liste = []
    for rezervasyon in rezervasyonlar:
        liste.append({"id": rezervasyon.id, "adi": str(rezervasyon), "aciklama": rezervasyon.aciklama})
    return JsonResponse(data={"data": liste, "status": "success", "message": "Başarılı"}, safe=False)


@login_required
def bekleyen_musteri_modal_getir_ajax(request):
    beklenen_gun = request.GET.get("beklenen_gun", None)
    beklenen_saat = request.GET.get("beklenen_saat", None)
    if beklenen_saat and beklenen_saat:
        gun = GunlerModel.objects.filter(adi=beklenen_gun).first()
        saat = SaatlerModel.objects.filter(baslangic_degeri=beklenen_saat + ":00").first()
        rezervasyonlar = bekleyen_musteri_getir(None, gun, saat)
    else:
        rezervasyonlar = bekleyen_musteri_getir(request.GET.get("tarih_saat"))
    html = render_to_string(
        "calendarapp/rezervasyon/partials/_bekleyen_listesi_modal.html", {"list": rezervasyonlar})
    return JsonResponse(data={"html": html, "status": "success", "message": "Başarılı"}, safe=False)


def bekleyen_musteri_getir(tarih_saat=None, gun=None, saat=None):
    gunun_saati = datetime.strptime(tarih_saat, "%Y-%m-%dT%H:%M:%S").time() if tarih_saat else datetime.now().time()
    haftanini_gunu = datetime.strptime(tarih_saat,
                                       "%Y-%m-%dT%H:%M:%S").weekday() if tarih_saat else datetime.now().weekday()
    gun = GunlerModel.objects.filter(haftanin_gunu=haftanini_gunu).first() if not gun else gun
    saat = SaatlerModel.objects.filter(baslangic_degeri=gunun_saati).first() if not saat else saat
    rezervasyonlar = RezervasyonModel.objects.filter(
        Q(gunler=gun, saatler=saat) |
        Q(gunler=gun, saatler__isnull=True) |
        Q(gunler__isnull=True, saatler=saat) |
        Q(gunler__isnull=True, saatler__isnull=True))
    return rezervasyonlar
