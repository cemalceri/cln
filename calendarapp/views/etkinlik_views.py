from itertools import chain

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta, datetime, date
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from calendarapp.forms.etkinlik_forms import EtkinlikForm

from calendarapp.models.Enums import KatilimDurumuEnum, AbonelikTipiEnum, GunEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, PaketKullanimModel, UyePaketModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from django.contrib import messages

from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import GrupModel, UyeGrupModel
from calendarapp.utils import formErrorsToText
import json


@login_required
def index(request):
    kortlar = KortModel.objects.all().order_by("id")
    saatler = []
    ilk_4_kort = kortlar[:4]
    ikinci_4_kort = kortlar[4:8]
    ucuncu_4_kort = kortlar[8:12]
    dorduncu_4_kort = kortlar[12:16]
    for i in range(9, 24):
        saatler.append(i)
    context = {
        "saatler": saatler,
        "kortlar": kortlar,
        "ilk_4_kort": ilk_4_kort,
        "ikinci_4_kort": ikinci_4_kort,
        "ucuncu_4_kort": ucuncu_4_kort,
        "dorduncu_4_kort": dorduncu_4_kort,
    }
    return render(request, "calendarapp/etkinlik/index.html", context)


@login_required
def gunun_etkinlikleri_ajax(request):
    etkinlikler = EtkinlikModel.objects.getir_bugunun_etkinlikleri().order_by("baslangic_tarih_saat")
    kortlar = KortModel.objects.all()
    list = []
    for item in kortlar:
        list.append({
            "kort_id": item.id,
            "kort_adi": item.adi,
            "max_etkinlik_sayisi": item.max_etkinlik_sayisi,
            "etkinlikler": [],
        })
    for etkinlik in etkinlikler:
        for item in list:
            if etkinlik.kort_id == item["kort_id"]:
                item["etkinlikler"].append({
                    "baslangic_saati": etkinlik.baslangic_tarih_saat.strftime("%H:%M"),
                    "bitis_saati": etkinlik.bitis_tarih_saat.strftime("%H:%M"),
                    "grup_adi": etkinlik.grup.__str__()[0:15],
                    "grup_id": etkinlik.grup.id,
                    "id": etkinlik.id,
                    "sure": int((etkinlik.bitis_tarih_saat - etkinlik.baslangic_tarih_saat).seconds / 60),
                    "renk": etkinlik.top_rengi,
                })
    return JsonResponse(data={"status": "success", "list": list})


@login_required(login_url="signup")
def getir_etkinlik_bilgisi_ajax(request):
    id = request.GET.get("id")
    event = EtkinlikModel.objects.get(id=id)
    event_dict = to_dict(event)
    return JsonResponse(event_dict)


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


@login_required()
def sil_etkinlik_ajax(request):
    id = request.GET.get("id")
    etklik = EtkinlikModel.objects.filter(pk=id).first()
    abonelik_sil(etklik)
    etklik.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


@login_required()
def sil_etkinlik(request, id):
    etklik = EtkinlikModel.objects.filter(pk=id).first()
    abonelik_sil(etklik)
    etklik.delete()
    messages.success(request, "Etkinlik silindi.")
    return redirect("dashboard")


@login_required(login_url="signup")
def sil_etkinlik_serisi_ajax(request):
    id = request.GET.get("id")
    etkinlik_list = EtkinlikModel.objects.filter(
        Q(pk=id) | Q(ilk_etkinlik_id=id, baslangic_tarih_saat__gte=datetime.now().date()))
    for etkinlik in etkinlik_list:
        abonelik_sil(etkinlik)
        etkinlik.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik serisi silindi."})


@login_required
def takvim_getir(request, kort_id=None):
    kort = KortModel.objects.filter(pk=kort_id).first()
    form = EtkinlikForm()
    kortlar = KortModel.objects.all().order_by("id")
    events = EtkinlikModel.objects.filter(kort_id=kort_id) if kort_id else []
    bugunun_etkinlikleri = EtkinlikModel.objects.getir_bugun_devam_eden_etkinlikler(kort_id=kort_id)
    event_list = []
    # start: '2020-09-16T16:00:00'
    for event in events:
        event_list.append(
            {
                "id": event.id,
                "title": event.grup.__str__(),
                "start": event.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "backgroundColor": event.top_rengi,
                # "eventColor": event.renk,
            }
        )
    context = {"form": form, "etkinlikler": event_list, "kortlar": kortlar,
               "secili_kort": kort,
               "bugunun_etkinlikleri": bugunun_etkinlikleri}
    return render(request, 'calendarapp/etkinlik/takvim.html', context)


@login_required
def kaydet_etkinlik_ajax(request):
    form = EtkinlikForm(request.POST)
    if form.is_valid():
        result = etkinlik_kaydi_hata_var_mi(form)
        if result:
            return result
        if form.cleaned_data["pk"] and form.cleaned_data["pk"] > 0:
            eski_etkinlik = EtkinlikModel.objects.get(id=form.cleaned_data["pk"])
            if form.cleaned_data["abonelik_tipi"] != eski_etkinlik.abonelik_tipi:
                return JsonResponse(data={"status": "error",
                                          "message": "Abonelik tipi güncellenemez. Lütfen etkinliği silerek yenisini oluşturunuz."})
            abonelik_guncelle(form, eski_etkinlik)
            form = EtkinlikForm(data=request.POST, instance=eski_etkinlik)
            form.save()
        else:
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            abonelik_olustur(item)
        return JsonResponse(data={"status": "success", "message": "Etkinlik kaydedildi."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, EtkinlikModel)})


def etkinlik_kaydi_hata_var_mi(form):
    mesaj = ""
    if form.cleaned_data["baslangic_tarih_saat"] > form.cleaned_data["bitis_tarih_saat"]:
        mesaj = "Etkinlik başlangıç tarihi bitiş tarihinden sonra olamaz."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if ayni_saatte_etkinlik_uygun_mu(form.cleaned_data["baslangic_tarih_saat"], form.cleaned_data["bitis_tarih_saat"],
                                     form.data["kort"], form.cleaned_data["pk"]):
        mesaj = "Bu kort aynı saat için maksimimum etkinlik sayısına ulaştı."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if form.cleaned_data["abonelik_tipi"] == AbonelikTipiEnum.Paket.value:
        uyeler = paket_uyeligi_olmayan_grup_uyesi(form)
        if uyeler:
            mesaj = uyeler + " paket kaydı olmadığı için etkinlik eklenemez."
            return JsonResponse(data={"status": "error", "message": mesaj})
    return False


def paket_uyeligi_olmayan_grup_uyesi(form):
    grup_id = form.data["grup" or None]
    uye_grubu = UyeGrupModel.objects.filter(grup_id=grup_id)
    uyeler = ""
    for item in uye_grubu:
        abonelik_paket_listesi = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True)
        if not abonelik_paket_listesi.exists():
            uyeler += str(item.uye) + ", "
    if uyeler != "":
        return uyeler[:-2]
    return False


def ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, kort_id, etkinlik_id=None):
    kort = KortModel.objects.get(id=kort_id)
    result = EtkinlikModel.objects.filter(Q(kort_id=kort_id) & (
            Q(baslangic_tarih_saat__lt=baslangic_tarih_saat,
              bitis_tarih_saat__gt=baslangic_tarih_saat) |  # başlangıç saati herhangi bir etkinliğin içinde olan
            Q(baslangic_tarih_saat=baslangic_tarih_saat,
              bitis_tarih_saat=bitis_tarih_saat) |  # başlangıç ve bitiş tarihi aynı olan
            Q(baslangic_tarih_saat__lt=bitis_tarih_saat, bitis_tarih_saat__gt=bitis_tarih_saat) |
            # bitiş tarihi herhangi bir etkinliğin içinde olan
            Q(baslangic_tarih_saat__gte=baslangic_tarih_saat, bitis_tarih_saat__lte=bitis_tarih_saat))
                                          # balangıç ve bitiş saati bizim etkinliğin arasında olan
                                          ).exclude(id=etkinlik_id)
    return result.count() > kort.max_etkinlik_sayisi - 1


# def etkinlik_tekrar_sayisi_kadar_ekle(request, form, etkinlik_id):
#     tekrar_sayisi = form.cleaned_data["tekrar"]
#     baslangic_tarih_saat = form.cleaned_data["baslangic_tarih_saat"]
#     bitis_tarih_saat = form.cleaned_data["bitis_tarih_saat"]
#     baslik = form.cleaned_data["baslik"]
#     if tekrar_sayisi and tekrar_sayisi > 0:
#         for i in range(tekrar_sayisi):
#             form.cleaned_data["baslangic_tarih_saat"] = baslangic_tarih_saat + timedelta(days=7 * (i + 1))
#             form.cleaned_data["bitis_tarih_saat"] = bitis_tarih_saat + timedelta(days=7 * (i + 1))
#             form.cleaned_data["baslik"] = baslik + " - Tekrar " + str(i + 1) + ". Hafta"
#             if not ayni_saatte_etkinlik_uygun_mu(form.cleaned_data["baslangic_tarih_saat"],
#                                                  form.cleaned_data["bitis_tarih_saat"], form.data["kort"]):
#                 item = EtkinlikForm(data=form.cleaned_data).save(commit=False)
#                 item.user = request.user
#                 item.ilk_etkinlik_id = etkinlik_id
#                 item.save()
#

@login_required
def saat_guncelle_etkinlik_ajax(request):
    id = request.GET.get("id")
    baslangic_tarih_saat = request.GET.get("baslangic_tarih_saat")
    bitis_tarih_saat = request.GET.get("bitis_tarih_saat")
    etkinlik = EtkinlikModel.objects.filter(pk=id).first()
    if ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, etkinlik.kort_id, id):
        return JsonResponse(
            data={"status": "error", "message": "Bu kort aynı saat için maksimimum etkinlik sayısına ulaştı."})
    etkinlik.baslangic_tarih_saat = baslangic_tarih_saat
    etkinlik.bitis_tarih_saat = bitis_tarih_saat
    etkinlik.save()
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})


@login_required
def etkinlik_tamamlandi_ajax(request):
    "TO DO:Burası yetkiler tanımlandığında düzenlecek. İşlemi yapan yönetici ise paket kullanım tablosuna kayıt atılacak."
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if etkinlik.bitis_tarih_saat > datetime.now():
            return JsonResponse(
                data={"status": "error", "message": "Etkinlik bitiş saatinden önce tamamlandı hale getirelemez."})
        uye_grup = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
        if etkinlik.abonelik_tipi == AbonelikTipiEnum.Paket.value:
            for item in uye_grup:
                paket = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True).first()
                if paket and not PaketKullanimModel.objects.filter(uye_paket_id=paket.id, etkinlik_id=etkinlik.id,
                                                                   uye_id=item.uye_id).exists():
                    PaketKullanimModel.objects.create(uye_paket_id=paket.id, etkinlik_id=etkinlik.id,
                                                      uye_id=item.uye_id, user=request.user)
        etkinlik.tamamlandi_yonetici = True
        etkinlik.save()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
    except Exception as e:
        return JsonResponse(data={"status": "error", "message": "Hata oluştu." + e.__str__()})


@login_required
def etkinlik_tamamlandi_iptal_ajax(request):
    "TO DO:Burası yetkiler tanımlandığında düzenlecek. İşlemi yapan yönetici ise paket kullanım tablosuna kayıt atılacak."
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        uye_grup = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
        if etkinlik.abonelik_tipi == AbonelikTipiEnum.Paket.value:
            for item in uye_grup:
                PaketKullanimModel.objects.filter(uye_id=item.uye_id, etkinlik_id=etkinlik.id).delete()
        etkinlik.tamamlandi_yonetici = False
        etkinlik.save()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
    except Exception as e:
        return JsonResponse(data={"status": "error", "message": "Hata oluştu." + e.__str__()})


# @login_required
# def katilim_ekle(request, id, uye_id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         if etkinlik.bitis_tarih_saat > datetime.now():
#             messages.error(request, "Etkinlik bitiş saatinden önce tamamlandı hale getirelemez.")
#             return redirect("calendarapp:profil_uye", uye_id)
#         if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id).exists():
#             EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye_id=uye_id,
#                                                 katilim_durumu=KatilimDurumuEnum.Katıldı.value, user=request.user)
#             # Bütün herkes katılım listesinde varsa etkinlik tamamlandı işaretle
#             herkes_katildi_mi = True
#             for uye_grubu in etkinlik.grup.grup_uyegrup_relations.all():
#                 if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye=uye_grubu.uye).exists():
#                     herkes_katildi_mi = False
#                     break
#             if herkes_katildi_mi:
#                 etkinlik.tamamlandi_mi = True
#                 etkinlik.save()
#             messages.success(request, "İşlem Başarılı.")
#         return redirect("calendarapp:profil_uye", uye_id)
#     except Exception as e:
#         messages.error(request, "Hata oluştu." + e.__str__())
#         return redirect("calendarapp:profil_uye", uye_id)


# @login_required
# def iptal_et(request, id, uye_id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id).exists():
#             EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye_id=uye_id,
#                                                 katilim_durumu=KatilimDurumuEnum.İptal.value, user=request.user)
#         messages.success(request, "İşlem Başarılı.")
#         return redirect("calendarapp:profil_uye", uye_id)
#     except Exception as e:
#         messages.error(request, "Hata oluştu." + e.__str__())
#         return redirect("calendarapp:profil_uye", uye_id)


# @login_required
# def iptal_et_by_antrenor(request, id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik).exists():
#             for item in UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id):
#                 EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye=item.uye,
#                                                     katilim_durumu=KatilimDurumuEnum.İptal.value, user=request.user)
#         messages.success(request, "İşlem Başarılı.")
#         return redirect("calendarapp:profil_antrenor", etkinlik.antrenor_id)
#     except Exception as e:
#         messages.error(request, "Hata oluştu." + e.__str__())
#         return redirect("calendarapp:index_antrenor")


# @login_required
# def iptal_geri_al(request, id, uye_id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         iptal_edilen = EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id,
#                                                            katilim_durumu=KatilimDurumuEnum.İptal.value)
#         if iptal_edilen.exists():
#             iptal_edilen.delete()
#         messages.success(request, "İşlem Başarılı.")
#         return redirect("calendarapp:profil_uye", uye_id)
#     except Exception as e:
#         messages.error(request, "Hata oluştu." + e.__str__())
#         return redirect("calendarapp:profil_uye", uye_id)
#
#
# @login_required
# def iptal_geri_al_by_antrenor(request, id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         iptal_edilen = EtkinlikKatilimModel.objects.filter(etkinlik_id=id,
#                                                            katilim_durumu=KatilimDurumuEnum.İptal.value)
#         if iptal_edilen.exists():
#             iptal_edilen.delete()
#         messages.success(request, "İşlem Başarılı.")
#         return redirect("calendarapp:profil_antrenor", etkinlik.antrenor_id)
#     except Exception as e:
#         messages.error(request, "Hata oluştu." + e.__str__())
#         return redirect("calendarapp:profil_antrenor")


@login_required
def etkinlik_detay_getir_ajax(request):
    etkinlik_id = request.GET.get("etkinlik_id")
    etkinlik = EtkinlikModel.objects.filter(pk=etkinlik_id).first()
    if etkinlik:
        html = render_to_string('calendarapp/etkinlik/_detay_modal.html', {"etkinlik": etkinlik})
    return JsonResponse(data={"status": "success", "messages": "İşlem başarılı", "html": html})


@login_required
def abonelik_olustur(etkinlik):
    uye_grubu = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
    haftaninin_gunu = etkinlik.baslangic_tarih_saat.weekday()
    gun_adi = gun_adi_getir(haftaninin_gunu)
    for item in uye_grubu:
        if not UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                               baslangic_tarih_saat=etkinlik.baslangic_tarih_saat).exists():
            UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu, gun_adi=gun_adi,
                                            baslangic_tarih_saat=etkinlik.baslangic_tarih_saat, grup=etkinlik.grup,
                                            bitis_tarih_saat=etkinlik.bitis_tarih_saat,
                                            aktif_mi=True, kort=etkinlik.kort, user=etkinlik.user)


def abonelik_guncelle(yeni_etkinlik_form, eski_etkinlik):
    if yeni_etkinlik_form.cleaned_data["grup"] == eski_etkinlik.grup:  # Grup değişmediyse aşağıdaki işlemleri yap
        uye_grubu = UyeGrupModel.objects.filter(grup_id=eski_etkinlik.grup_id)
        haftaninin_gunu = eski_etkinlik.baslangic_tarih_saat.weekday()
        for item in uye_grubu:
            abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                       grup_id=eski_etkinlik.grup_id,
                                                       baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat)
            if abonelik.exists():  # Grup üyesinin eskidende bu grubun içindeyse zaten abonelik kaydı vardır. O yüzden mevcut kaydı güncelle
                abonelik = abonelik.first()
                abonelik.baslangic_tarih_saat = yeni_etkinlik_form.cleaned_data["baslangic_tarih_saat"]
                abonelik.bitis_tarih_saat = yeni_etkinlik_form.cleaned_data["bitis_tarih_saat"]
                abonelik.kort = yeni_etkinlik_form.cleaned_data["kort"]
                haftaninin_gunu = yeni_etkinlik_form.cleaned_data["baslangic_tarih_saat"].weekday()
                gun_adi = gun_adi_getir(haftaninin_gunu)
                abonelik.gun_adi = gun_adi
                abonelik.save()
            else:  # Grup üyesinin eski tarih saatte üyeliği yok ise demek ki yeni gruba eklenmiş. Yeni abonelik kaydı oluştur.
                haftaninin_gunu = yeni_etkinlik_form.cleaned_data["baslangic_tarih_saat"].weekday()
                gun_adi = gun_adi_getir(haftaninin_gunu)
                UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu, gun_adi=gun_adi,
                                                baslangic_tarih_saat=yeni_etkinlik_form.cleaned_data[
                                                    "baslangic_tarih_saat"],
                                                grup=yeni_etkinlik_form.cleaned_data["grup"],
                                                bitis_tarih_saat=yeni_etkinlik_form.cleaned_data["bitis_tarih_saat"],
                                                aktif_mi=True, kort=yeni_etkinlik_form.cleaned_data["kort"])
    else:  # Grup değiştiyse eski grup üyelerinin aboneliklerini sil, yeni üyelere abonelik oluştur
        eski_uye_grubu = UyeGrupModel.objects.filter(grup_id=eski_etkinlik.grup_id)
        yeni_uye_grubu = UyeGrupModel.objects.filter(grup_id=yeni_etkinlik_form.cleaned_data["grup"].id)
        haftaninin_gunu = eski_etkinlik.baslangic_tarih_saat.weekday()
        for item in eski_uye_grubu:
            abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                       grup_id=eski_etkinlik.grup_id,
                                                       baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat)
            if abonelik.exists():
                abonelik = abonelik.first()
                abonelik.delete()
        for item in yeni_uye_grubu:
            if not UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                   baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat).exists():
                UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat,
                                                grup=yeni_etkinlik_form.cleaned_data["grup"],
                                                bitis_tarih_saat=eski_etkinlik.bitis_tarih_saat,
                                                aktif_mi=True, kort=eski_etkinlik.kort)


def abonelik_sil(etkinlik):
    uye_grubu = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
    haftaninin_gunu = etkinlik.baslangic_tarih_saat.weekday()
    for item in uye_grubu:
        abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                   baslangic_tarih_saat=etkinlik.baslangic_tarih_saat)
        if abonelik.exists():
            abonelik = abonelik.first()
            abonelik.delete()


def gun_adi_getir(haftanin_gunu):
    if haftanin_gunu == 0:
        return "Pazartesi"
    elif haftanin_gunu == 1:
        return "Salı"
    elif haftanin_gunu == 2:
        return "Çarşamba"
    elif haftanin_gunu == 3:
        return "Perşembe"
    elif haftanin_gunu == 4:
        return "Cuma"
    elif haftanin_gunu == 5:
        return "Cumartesi"
    elif haftanin_gunu == 6:
        return "Pazar"
