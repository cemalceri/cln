from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from calendarapp.enums import GrupOdemeSekliEnum
from calendarapp.forms.uye_forms import UyeGrupKayitForm
from calendarapp.models.concrete.uye import UyeGrupModel, GrupModel, UyeModel
from calendarapp.utils import formErrorsToText


@login_required
def index_grup(request):
    form = GrupModel.objects.filter(tekil_mi=False).order_by('-id')
    return render(request, "calendarapp/grup/index.html", {"list": form})


@login_required
def kaydet_grup(request, id=None):
    if request.method == 'POST':
        if UyeGrupModel.objects.filter(grup_id=request.POST.get("grup_id"), uye_id=request.POST.get("uye_id")).exists():
            return JsonResponse(data={"status": "error", "message": "Üye gruba zaten kayıtlı."})
        if int(request.POST.get("grup_id")) > 0:
            UyeGrupModel.objects.create(grup_id=request.POST.get("grup_id"), uye_id=request.POST.get("uye_id"),
                                        odeme_sekli=request.POST.get("odeme_sekli"))
            grup_id = request.POST.get("grup_id")
        else:
            grup = GrupModel.objects.create(adi="grup", tekil_mi=False)
            grup_id = grup.id
            UyeGrupModel.objects.create(grup=grup, uye_id=request.POST.get("uye_id"),
                                        odeme_sekli=request.POST.get("odeme_sekli"))
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "grup_id": grup_id})
    else:
        uyeler = UyeModel.objects.filter(onaylandi_mi=True)
        odemeler_tipleri = GrupOdemeSekliEnum.choices()
        uye_grup_listesi = UyeGrupModel.objects.filter(grup_id=id)
        return render(request, "calendarapp/grup/kaydet.html",
                      {'uyeler': uyeler, 'odemeler_tipleri': odemeler_tipleri, 'grup_id': id,
                       'uye_grup_listesi': uye_grup_listesi})


@login_required
def detay_grup(request, id):
    pass


@login_required
def sil_grup(request, id):
    GrupModel.objects.filter(pk=id).delete()
    return redirect("calendarapp:index_grup")


@login_required
def sil_grup_uyesi(request):
    UyeGrupModel.objects.filter(grup_id=request.POST.get("grup_id"),
                                uye_id=request.POST.get("uye_id")).first().delete()
    # Son üye silindiğinde grup silinir. dolayısıyla sayfada tekrar üye eklemeye çalışınca hata alınır.
    # Yeni grup kaydı gibi olması için grup id'si 0 gönderilir.
    grup_id = 0 if UyeGrupModel.objects.filter(grup_id=request.POST.get("grup_id")).count() ==0 else request.POST.get("grup_id")
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "grup_id": grup_id})
