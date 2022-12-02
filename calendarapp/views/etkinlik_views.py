from itertools import chain

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta, datetime, date
from django.contrib.auth.decorators import login_required
from calendarapp.forms.etkinlik_forms import EtkinlikForm

from calendarapp.models.Enums import KatilimDurumuEnum, AbonelikTipiEnum, GunEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, PaketKullanimModel, UyePaketModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel, EtkinlikKatilimModel
from django.contrib import messages

from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import GrupModel, UyeGrupModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    etkinlikler = EtkinlikModel.objects.getir_bugunun_etkinlikleri()
    # kortlarin_bos_saatleri = kortlarin_bos_saatlerini_getir(datetime.now())
    kortlar_ilk_alti = KortModel.objects.all()[:6]
    kortlar_ikinci_alti = KortModel.objects.all()[6:12]
    kortlar_ucuncu_alti = KortModel.objects.all()[12:18]
    context = {
        "kortlar_ilk_alti": kortlar_ilk_alti,
        "kortlar_ikinci_alti": kortlar_ikinci_alti,
        "etkinlikler": etkinlikler,
        "kortlar_ucuncu_alti": kortlar_ucuncu_alti,
        # "kortlarin_bos_saatleri": kortlarin_bos_saatleri
    }
    return render(request, "calendarapp/etkinlik/index.html", context)


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


@login_required(login_url="signup")
def sil_etkinlik_ajax(request):
    id = request.GET.get("id")
    EtkinlikModel.objects.filter(pk=id).first().delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


@login_required()
def sil_etkinlik(request, id):
    EtkinlikModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Etkinlik silindi.")
    return redirect("dashboard")


@login_required(login_url="signup")
def sil_etkinlik_serisi_ajax(request):
    id = request.GET.get("id")
    etkinlik = EtkinlikModel.objects.filter(pk=id).first()
    etkinlik_list = EtkinlikModel.objects.filter(
        Q(pk=id) | Q(pk=etkinlik.ilk_etkinlik_id) | Q(ilk_etkinlik_id=etkinlik.ilk_etkinlik_id,
                                                      ilk_etkinlik_id__isnull=False) | Q(
            ilk_etkinlik_id=id, ilk_etkinlik_id__isnull=False))
    if etkinlik_list:
        etkinlik_list.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


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
        mesaj = "Seçilen tarih saate başka etkinlik eklenemez."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if form.cleaned_data["abonelik_tipi"] == AbonelikTipiEnum.Paket.value:
        uye = paket_uyeligi_olmayan_grup_uyesi(form)
        if uye:
            mesaj = "Grupta bulunan '" + str(
                uye) + "' üyesinin uygun paket/abonelik kaydı olmadığı için etkinlik eklenemez."
            return JsonResponse(data={"status": "error", "message": mesaj})
    return False


def paket_uyeligi_olmayan_grup_uyesi(form):
    grup_id = form.data["grup" or None]
    uye_grubu = UyeGrupModel.objects.filter(grup_id=grup_id)
    for item in uye_grubu:
        abonelik_paket_listesi = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True)
        if not abonelik_paket_listesi.exists():
            return str(item.uye)
    return None


def ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, kort_id, etkinlik_id=None):
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
    return result.count() > 3


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
        return JsonResponse(data={"status": "error", "message": "Seçilen tarih saatlerde başka etkinlik kayıtlı."})
    etkinlik.baslangic_tarih_saat = baslangic_tarih_saat
    etkinlik.bitis_tarih_saat = bitis_tarih_saat
    etkinlik.save()
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})


@login_required
def etkinlik_tamamlandi_ajax(request):
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if etkinlik.bitis_tarih_saat > datetime.now():
            return JsonResponse(
                data={"status": "error", "message": "Etkinlik bitiş saatinden önce tamamlandı hale getirelemez."})
        uye_grup = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
        for item in uye_grup:
            paket = UyeAbonelikModel.objects.filter(uye=item.uye, paket__isnull=False, aktif_mi=True, ).order_by("-id")
            if paket.exists():
                PaketKullanimModel.objects.create(uye=item.uye, abonelik=paket.first(), etkinlik=etkinlik,
                                                  user=request.user)
            EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye=item.uye,
                                                katilim_durumu=KatilimDurumuEnum.Katıldı.value,
                                                user=request.user)
        etkinlik.tamamlandi_mi = True
        etkinlik.save()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
    except Exception as e:
        return JsonResponse(data={"status": "error", "message": "Hata oluştu." + e.__str__()})


@login_required
def katilim_ekle(request, id, uye_id):
    try:
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if etkinlik.bitis_tarih_saat > datetime.now():
            messages.error(request, "Etkinlik bitiş saatinden önce tamamlandı hale getirelemez.")
            return redirect("calendarapp:profil_uye", uye_id)
        if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id).exists():
            EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye_id=uye_id,
                                                katilim_durumu=KatilimDurumuEnum.Katıldı.value, user=request.user)
            # Bütün herkes katılım listesinde varsa etkinlik tamamlandı işaretle
            herkes_katildi_mi = True
            for uye_grubu in etkinlik.grup.grup_uyegrup_relations.all():
                if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye=uye_grubu.uye).exists():
                    herkes_katildi_mi = False
                    break
            if herkes_katildi_mi:
                etkinlik.tamamlandi_mi = True
                etkinlik.save()
            messages.success(request, "İşlem Başarılı.")
        return redirect("calendarapp:profil_uye", uye_id)
    except Exception as e:
        messages.error(request, "Hata oluştu." + e.__str__())
        return redirect("calendarapp:profil_uye", uye_id)


@login_required
def iptal_et(request, id, uye_id):
    try:
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id).exists():
            EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye_id=uye_id,
                                                katilim_durumu=KatilimDurumuEnum.İptal.value, user=request.user)
        messages.success(request, "İşlem Başarılı.")
        return redirect("calendarapp:profil_uye", uye_id)
    except Exception as e:
        messages.error(request, "Hata oluştu." + e.__str__())
        return redirect("calendarapp:profil_uye", uye_id)


@login_required
def iptal_et_by_antrenor(request, id):
    try:
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik).exists():
            for item in UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id):
                EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye=item.uye,
                                                    katilim_durumu=KatilimDurumuEnum.İptal.value, user=request.user)
        messages.success(request, "İşlem Başarılı.")
        return redirect("calendarapp:profil_antrenor", etkinlik.antrenor_id)
    except Exception as e:
        messages.error(request, "Hata oluştu." + e.__str__())
        return redirect("calendarapp:index_antrenor")


@login_required
def iptal_geri_al(request, id, uye_id):
    try:
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        iptal_edilen = EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id,
                                                           katilim_durumu=KatilimDurumuEnum.İptal.value)
        if iptal_edilen.exists():
            iptal_edilen.delete()
        messages.success(request, "İşlem Başarılı.")
        return redirect("calendarapp:profil_uye", uye_id)
    except Exception as e:
        messages.error(request, "Hata oluştu." + e.__str__())
        return redirect("calendarapp:profil_uye", uye_id)


@login_required
def iptal_geri_al_by_antrenor(request, id):
    try:
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        iptal_edilen = EtkinlikKatilimModel.objects.filter(etkinlik_id=id,
                                                           katilim_durumu=KatilimDurumuEnum.İptal.value)
        if iptal_edilen.exists():
            iptal_edilen.delete()
        messages.success(request, "İşlem Başarılı.")
        return redirect("calendarapp:profil_antrenor", etkinlik.antrenor_id)
    except Exception as e:
        messages.error(request, "Hata oluştu." + e.__str__())
        return redirect("calendarapp:profil_antrenor")


# @login_required
# def kortlarin_bos_saatlerini_getir(request):
#     kortlarin_bos_saatleri = {}
#     time_range = range(9, 24)
#     dakikalar = [00, 15, 30, 45]
#     for kort in KortModel.objects.all():
#         kortlarin_bos_saatleri[kort.id] = []
#         for saat in time_range:
#             for dakika in dakikalar:
#                 sorgu_saati = datetime.today().replace(hour=saat, minute=dakika, second=0, microsecond=0)
#                 etkinlik = EtkinlikModel.objects.filter(kort_id=kort.id,
#                                                         baslangic_tarih_saat=sorgu_saati)
#                 if not etkinlik.exists():
#                     kortlarin_bos_saatleri[kort.id].append(sorgu_saati)
#     return JsonResponse(
#         data={"status": "success", "messages": "İşlem başarılı", "data": kortlarin_bos_saatleri})


@login_required
def kortlarin_bos_saatlerini_getir(request):
    kortlarin_bos_saatleri = {}
    time_range = range(9, 24)
    dakikalar = [00, 15, 30, 45]
    bugunun_etkinlikleri = EtkinlikModel.objects.getir_bugunun_etkinlikleri()
    kortlar = KortModel.objects.all()
    for kort in kortlar:
        kortlarin_bos_saatleri[kort.id] = []
        for saat in time_range:
            for dakika in dakikalar:
                sorgu_saati = datetime.today().replace(hour=saat, minute=dakika, second=0, microsecond=0)
                etkinlik = bugunun_etkinlikleri.filter(kort_id=kort.id, baslangic_tarih_saat__lte=sorgu_saati,
                                                       bitis_tarih_saat__gt=sorgu_saati)
                if not etkinlik.exists():
                    kortlarin_bos_saatleri[kort.id].append(sorgu_saati)
    return JsonResponse(
        data={"status": "success", "messages": "İşlem başarılı", "data": kortlarin_bos_saatleri})


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


def gun_adi_getir(haftanin_gunu):
    value = ""
    if haftanin_gunu == 0:
        value = "Pazartesi"
    elif haftanin_gunu == 1:
        value = "Salı"
    elif haftanin_gunu == 2:
        value = "Çarşamba"
    elif haftanin_gunu == 3:
        value = "Perşembe"
    elif haftanin_gunu == 4:
        value = "Cuma"
    elif haftanin_gunu == 5:
        value = "Cumartesi"
    elif haftanin_gunu == 6:
        value = "Pazar"
    return value
