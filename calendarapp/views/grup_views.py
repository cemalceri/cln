from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from calendarapp.models.Enums import GrupOdemeSekliEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel
from calendarapp.models.concrete.uye import UyeGrupModel, GrupModel, UyeModel


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
            grup_adi = request.POST.get("adi" or None)
            grup = GrupModel.objects.create(adi=grup_adi, tekil_mi=False)
            grup_id = grup.id
            UyeGrupModel.objects.create(grup=grup, uye_id=request.POST.get("uye_id"),
                                        odeme_sekli=request.POST.get("odeme_sekli"))
        uyeye_grubun_aboneliklerini_ekle(request, request.POST.get("uye_id"), grup_id)
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "grup_id": grup_id})
    else:
        uyeler = UyeModel.objects.filter(onaylandi_mi=True)
        odemeler_tipleri = GrupOdemeSekliEnum.choices()
        uye_grup_listesi = UyeGrupModel.objects.filter(grup_id=id)
        grup_adi = GrupModel.objects.get(id=id).adi if id else None
        return render(request, "calendarapp/grup/kaydet.html",
                      {'uyeler': uyeler, 'odemeler_tipleri': odemeler_tipleri, 'grup_id': id,
                       'uye_grup_listesi': uye_grup_listesi, 'grup_adi': grup_adi})


@login_required
def guncelle_grup_adi(request):
    if request.method == 'POST':
        if int(request.POST.get("grup_id")) > 0:
            grup = GrupModel.objects.filter(id=request.POST.get("grup_id")).first()
            grup.adi = request.POST.get("adi")
            grup.save()
            return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
        else:
            return JsonResponse(data={"status": "error", "message": "Üye ekleyiniz."})


@login_required
def sil_grup(request, id):
    GrupModel.objects.filter(pk=id).delete()
    return redirect("calendarapp:index_grup")


@login_required
def sil_grup_uyesi(request):
    UyeGrupModel.objects.filter(grup_id=request.POST.get("grup_id"),
                                uye_id=request.POST.get("uye_id")).first().delete()
    uyeden_grubun_aboneliklerini_sil(request.POST.get("uye_id"), request.POST.get("grup_id"))
    # Son üye silindiğinde grup silinir. dolayısıyla sayfada tekrar üye eklemeye çalışınca hata alınır.
    # Yeni grup kaydı gibi olması için grup id'si 0 gönderilir.
    grup_id = 0 if UyeGrupModel.objects.filter(grup_id=request.POST.get("grup_id")).count() == 0 else request.POST.get(
        "grup_id")
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "grup_id": grup_id})


@login_required
def uyeye_grubun_aboneliklerini_ekle(request, uye_id, grup_id):
    uyelikler = UyeAbonelikModel.objects.filter(grup_id=grup_id)
    for uyelik in uyelikler:
        if not UyeAbonelikModel.objects.filter(uye_id=uye_id, grup_id=grup_id, haftanin_gunu=uyelik.haftanin_gunu,
                                               baslangic_tarih_saat=uyelik.baslangic_tarih_saat).exists():
            UyeAbonelikModel.objects.create(uye_id=uye_id, grup_id=uyelik.grup_id, kort=uyelik.kort,
                                            haftanin_gunu=uyelik.haftanin_gunu, gun_adi=uyelik.gun_adi,
                                            baslangic_tarih_saat=uyelik.baslangic_tarih_saat,
                                            bitis_tarih_saat=uyelik.bitis_tarih_saat, aktif_mi=uyelik.aktif_mi,
                                            user=request.user)


@login_required
def ara_ajax(request):
    aranan = request.GET.get("q")
    if aranan:
        grup = GrupModel.objects.filter(adi__icontains=aranan).order_by("adi")[0:10]
    else:
        grup = GrupModel.objects.all().order_by("-id")[0:10]
    liste = []
    for g in grup:
        liste.append({"id": g.id, "adi": g.adi})
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "list": liste})


def uyeden_grubun_aboneliklerini_sil(uye_id, grup_id):
    UyeAbonelikModel.objects.filter(uye_id=uye_id, grup_id=grup_id).delete()
