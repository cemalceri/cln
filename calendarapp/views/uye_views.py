from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from calendarapp.forms.muhasebe_forms import UyeParaHareketiKayitForm
from calendarapp.forms.uye_forms import UyeKayitForm, GencUyeKayitForm
from calendarapp.models.Enums import KatilimDurumuEnum, UyeTipiEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, UyePaketModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel, MuhasebeModel
from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = UyeModel.objects.all().order_by('-id')
    return render(request, "calendarapp/uye/index.html", {"uye_list": form})


@login_required
def kaydet(request, id=None, uye_tipi=None):
    if request.method == 'POST':
        entity = UyeModel.objects.filter(pk=id).first()
        uye_tipi = request.POST.get("uye_tipi")
        form = UyeKayitForm(request.POST,
                            instance=entity) if uye_tipi == UyeTipiEnum.Yetişkin.value else GencUyeKayitForm(
            request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            form.save_m2m()
            messages.success(request, "Üye kaydedildi.")
            return redirect("calendarapp:index_uye")
        else:
            messages.error(request, formErrorsToText(form.errors, UyeModel))
            return render(request, "calendarapp/uye/kaydet.html", context={'form': form})
    else:
        duzenleme_mi = False
        if id is not None:
            uye = UyeModel.objects.filter(pk=id).first()
            uye_tipi = uye.uye_tipi
            duzenleme_mi = True
            form = UyeKayitForm(instance=uye) if uye_tipi == UyeTipiEnum.Yetişkin.value else GencUyeKayitForm(
                instance=uye)
        elif uye_tipi is not None:
            form = UyeKayitForm() if uye_tipi == UyeTipiEnum.Yetişkin.value else GencUyeKayitForm()
        else:
            form = None
    return render(request, "calendarapp/uye/kaydet.html",
                  context={'form': form, 'uye_tipi': uye_tipi, 'duzenleme_mi': duzenleme_mi})


@login_required
def sil(request, id):
    UyeModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_uye")


@login_required
def profil(request, id):
    uye = UyeModel.objects.filter(pk=id).first()
    abonelikler = UyeAbonelikModel.objects.filter(uye_id=id)
    paketler = UyePaketModel.objects.filter(uye_id=id)
    gruplar = UyeGrupModel.objects.filter(uye_id=id).values_list('grup_id', flat=True)
    yapilacak_etkinlikler = EtkinlikModel.objects.filter(grup_id__in=gruplar, baslangic_tarih_saat__gt=datetime.now(
    )).order_by('baslangic_tarih_saat')
    yapilan_etkinlikler = EtkinlikModel.objects.filter(grup_id__in=gruplar, bitis_tarih_saat__lt=datetime.now(
    )).order_by('-baslangic_tarih_saat')
    iptal_etkinlikler = EtkinlikModel.objects.filter(grup_id__in=gruplar, iptal_mi=True).order_by(
        '-baslangic_tarih_saat')
    return render(request, "calendarapp/uye/profil.html",
                  {"uye": uye, "abonelikler": abonelikler, "paketler": paketler,
                   "yapilacak_etkinlikler": yapilacak_etkinlikler, "yapilan_etkinlikler": yapilan_etkinlikler,
                   "iptal_etkinlikler": iptal_etkinlikler})


@login_required
def muhasebe_uye(request, uye_id):
    if not MuhasebeModel.objects.filter(uye_id=uye_id, yil=datetime.now().year, ay=datetime.now().month).exists():
        MuhasebeModel.objects.create(uye_id=uye_id, yil=datetime.now().year, ay=datetime.now().month)
    muhasebe_list = MuhasebeModel.objects.filter(uye_id=uye_id).order_by('yil', 'ay')
    uye = UyeModel.objects.filter(pk=uye_id).first()
    return render(request, "calendarapp/uye/muhasebe.html", {"muhasebe_list": muhasebe_list, "uye": uye})


@login_required
def muhasebe_detay_modal_getir_ajax(request):
    yil = request.GET.get('yil')
    ay = request.GET.get('ay')
    uye_id = request.GET.get('uye_id')
    para_hareketleri = ParaHareketiModel.objects.filter(uye_id=uye_id, tarih__year=yil, tarih__month=ay).order_by('-id')
    html = render_to_string('calendarapp/uye/partials/_uye_muhasebe_detay.html', {'para_hareketleri': para_hareketleri})
    return JsonResponse(
        data={"status": "success", "message": "İşlem Başarılı.", "html": html})


@login_required
def muhasebe_odeme_modal_getir_ajax(request):
    yil = request.GET.get('yil')
    ay = request.GET.get('ay')
    uye_id = request.GET.get('uye_id')
    odeme_id = request.GET.get('odeme_id')
    tarih = datetime.strptime(f"{yil}-{ay}-01", "%Y-%m-%d")
    if odeme_id is not None:
        para_hareketi = ParaHareketiModel.objects.filter(pk=odeme_id).first()
        form = UyeParaHareketiKayitForm(instance=para_hareketi)
    else:
        form = UyeParaHareketiKayitForm(initial={'tarih': tarih, 'uye': uye_id})
    html = render_to_string('calendarapp/uye/partials/_uye_odeme_girisi.html', {'form': form, "uye_id": uye_id})
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "html": html})


@login_required
def kaydet_uye_odemesi_ajax(request):
    form = UyeParaHareketiKayitForm(request.GET)
    if form.is_valid():
        entity = form.save(commit=False)
        entity.user = request.user
        entity.save()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, ParaHareketiModel)})
