from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from calendarapp.models.Enums import ParaHareketTuruEnum
from calendarapp.models.concrete.muhasebe import ParaHareketiModel


@login_required
def index(request):
    form = ParaHareketiModel.objects.all().order_by('id')
    return render(request, "calendarapp/muhasebe/index.html", {"list": form})


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
        ParaHareketiModel.objects.create(paket_id=paket, aciklama=aciklama, tarih=tarih, tutar=tutar, uye_id=uye,
                                         hareket_turu=ParaHareketTuruEnum.Giris.value)
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})


@login_required
def getir_odeme_by_id_ajax(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print(id)
        odeme = ParaHareketiModel.objects.filter(pk=id).first()
        print(to_dict(odeme))
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "data": to_dict(odeme)})


@login_required
def detay_antrenor(request, id):
    pass


@login_required
def sil_uye_odemesi(request, id):
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
