from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect
from calendarapp.models.Enums import ParaHareketTuruEnum
from calendarapp.models.concrete.muhasebe import ParaHareketiModel


@login_required
def index(request):
    if request.method == "POST":
        baslangic_tarihi = request.POST.get("baslangic_tarihi" or None)
        bitis_tarihi = request.POST.get("bitis_tarihi" or None)
        tutar_max = request.POST.get("tutar_max" or None)
        tutar_min = request.POST.get("tutar_min" or None)
        para_girisleri = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Giris.value)
        para_cikislari = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Cikis.value)
        filtre_metni = ""
        if baslangic_tarihi:
            filtre_metni += "Başlangıç tarihi " + baslangic_tarihi + " tarihinden büyük, "
            para_girisleri = para_girisleri.filter(tarih__gte=baslangic_tarihi)
            para_cikislari = para_cikislari.filter(tarih__gte=baslangic_tarihi)
        if bitis_tarihi:
            filtre_metni += "Bitiş tarihi " + bitis_tarihi + " tarihinden küçük, "
            para_girisleri = para_girisleri.filter(tarih__lte=bitis_tarihi)
            para_cikislari = para_cikislari.filter(tarih__lte=bitis_tarihi)
        if tutar_min:
            filtre_metni += "Tutarı " + tutar_min + " TL'den büyük,  "
            para_girisleri = para_girisleri.filter(tutar__gte=tutar_min)
            para_cikislari = para_cikislari.filter(tutar__gte=tutar_min)
        if tutar_max:
            filtre_metni += "Tutarı " + tutar_max + " TL'den küçük, "
            para_girisleri = para_girisleri.filter(tutar__lte=tutar_max)
            para_cikislari = para_cikislari.filter(tutar__lte=tutar_max)
        toplam_giris = para_girisleri.aggregate(models.Sum('tutar'))['tutar__sum']
        toplam_cikis = para_cikislari.aggregate(models.Sum('tutar'))['tutar__sum']
        if filtre_metni == "":
            filtre_metni = "*Filtre uygulanmadan  tüm kayıtlar gösteriliyor."
        else:
            filtre_metni = "*" + filtre_metni + " kayıtları gösteriliyor."
        context = {
            "para_girisleri": para_girisleri,
            "para_cikislari": para_cikislari,
            "toplam_giris": toplam_giris,
            "toplam_cikis": toplam_cikis,
            "filtreMetni": filtre_metni
        }
        messages.success(request, "İşlem başarılı!")
        return render(request, "calendarapp/muhasebe/index.html", context)
    else:
        para_girisleri = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Giris.value).order_by(
            '-tarih')[0:100]
        para_cikislari = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Cikis.value).order_by(
            '-tarih')[0:100]
        toplam_giris = para_girisleri.aggregate(models.Sum('tutar'))['tutar__sum']
        toplam_cikis = para_cikislari.aggregate(models.Sum('tutar'))['tutar__sum']
        context = {
            "para_girisleri": para_girisleri,
            "para_cikislari": para_cikislari,
            "toplam_giris": toplam_giris,
            "toplam_cikis": toplam_cikis,
        }
        return render(request, "calendarapp/muhasebe/index.html", context)


@login_required
def kaydet_uye_odemesi_ajax(request):
    if request.method == 'POST':
        aciklama = request.POST.get('aciklama')
        tarih = request.POST.get('tarih')
        tutar = request.POST.get('tutar')
        uye = request.POST.get('uye')
        paket = request.POST.get('paket')
        if tutar is None or tutar == '':
            return JsonResponse({'status': 'error', 'message': 'Tutar boş olamaz.'})
        if tarih is None or tarih == '':
            return JsonResponse({'status': 'error', 'message': 'Tarih boş olamaz.'})
        if request.POST.get('id'):
            item = ParaHareketiModel.objects.get(id=request.POST.get('id'))
            item.aciklama = aciklama
            item.tarih = tarih
            item.tutar = tutar
            item.uye_id = uye
            item.paket_id = paket
            item.save()
        else:
            print(paket)
            print(aciklama)
            print(tarih)
            print(tutar)
            print(uye)
            ParaHareketiModel.objects.create(paket_id=paket, aciklama=aciklama, tarih=tarih, tutar=tutar, uye_id=uye,
                                             hareket_turu=ParaHareketTuruEnum.Giris.value)
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})


@login_required
def kaydet_antrenor_odemesi_ajax(request):
    if request.method == 'POST':
        aciklama = request.POST.get('aciklama')
        tarih = request.POST.get('tarih')
        tutar = request.POST.get('tutar')
        anternor = request.POST.get('antrenor')
        odeme_turu = request.POST.get('odeme_turu')
        if tutar is None or tutar == '':
            return JsonResponse({'status': 'error', 'message': 'Tutar boş olamaz.'})
        if tarih is None or tarih == '':
            return JsonResponse({'status': 'error', 'message': 'Tarih boş olamaz.'})
        if request.POST.get('id'):
            item = ParaHareketiModel.objects.get(id=request.POST.get('id'))
            item.aciklama = aciklama
            item.tarih = tarih
            item.odeme_turu = odeme_turu
            item.tutar = tutar
            item.antrenor_id = anternor
            item.save()
        else:
            ParaHareketiModel.objects.create(odeme_turu=odeme_turu, aciklama=aciklama, tarih=tarih, tutar=tutar,
                                             antrenor_id=anternor, hareket_turu=ParaHareketTuruEnum.Cikis.value)
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})


@login_required
def getir_odeme_by_id_ajax(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        odeme = ParaHareketiModel.objects.filter(pk=id).first()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "data": to_dict(odeme)})


@login_required
def sil_odeme(request, id):
    odeme = ParaHareketiModel.objects.filter(pk=id).first()
    uye_id = odeme.uye_id
    odeme.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:profil_uye", id=uye_id)


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data
