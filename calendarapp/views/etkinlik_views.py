from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta, datetime, date
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from calendarapp.forms.etkinlik_forms import EtkinlikForm, HaftalikPlanForm

from calendarapp.models.Enums import KatilimDurumuEnum, AbonelikTipiEnum, GunEnum, GunlerModel, SaatlerModel, RenkEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, PaketKullanimModel, UyePaketModel
from calendarapp.models.concrete.commons import gun_adi_getir, to_dict
from calendarapp.models.concrete.etkinlik import EtkinlikModel, HaftalikPlanModel
from django.contrib import messages

from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.models.concrete.uye import GrupModel, UyeGrupModel
from calendarapp.utils import formErrorsToText
import json

gunler = GunlerModel.objects.all()
saatler = SaatlerModel.objects.all()


@login_required
def index(request):
    tarih = datetime.now().date()
    context = index_sayfasi_icin_context_olustur(request, tarih)
    return render(request, "calendarapp/etkinlik/index.html", context)


@login_required
def index_getir_by_tarih(request, tarih):
    context = index_sayfasi_icin_context_olustur(request, tarih)
    return render(request, "calendarapp/etkinlik/index.html", context)


def index_sayfasi_icin_context_olustur(request, tarih):
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y-%m-%d").date()
    sorgulanan_haftanini_ilk_gunu = tarih - timedelta(days=datetime.now().weekday())
    haftanin_gunleri = []
    haftanin_gunleri_strf = []
    kortlar = KortModel.objects.all().order_by("id")
    for i in range(0, 7):
        haftanin_gunleri.append(sorgulanan_haftanini_ilk_gunu + timedelta(days=i))
        haftanin_gunleri_strf.append((sorgulanan_haftanini_ilk_gunu + timedelta(days=i)).strftime("%Y-%m-%d"))
    saatler = []
    dakikalar = ["00", "30"]
    for i in range(9, 24):
        for dk in dakikalar:
            saatler.append(str(i) + ":" + dk)
    html = ""
    islem = divmod(kortlar.count(), 4)
    bolum = islem[0]
    kalan = islem[1]
    for gun in haftanin_gunleri:
        baslangic = 0
        bitis = 4
        for i in range(bolum):
            html += render_to_string('calendarapp/etkinlik/partials/_gunluk_plan_icin_kortlar.html',
                                     {'kortlar': kortlar[baslangic:bitis], 'saatler': saatler, 'tarih': gun,
                                      'tarih_str': gun.strftime("%Y-%m-%d")})
            baslangic += 4
            bitis += 4
        if kalan > 0:
            html += render_to_string('calendarapp/etkinlik/partials/_gunluk_plan_icin_kortlar.html',
                                     {'kortlar': kortlar[baslangic:], 'saatler': saatler, 'tarih': gun,
                                      'tarih_str': gun.strftime("%Y-%m-%d")})
    context = {
        "kortlar": html,
        "haftanin_gunleri": haftanin_gunleri_strf,
    }
    return context


def saatler_ve_etkinlikler_dict_olustur(kort, etkinlikler, tarih, bekleyenler):
    saatler = []
    bucukSaatler = ["00", "30"]
    for i in range(9, 24):
        for t in bucukSaatler:
            sorgulanan_tarih_saat_baslangic = datetime.combine(tarih, datetime.min.time()).replace(hour=i).replace(
                minute=int(t))
            # sorgulanan_tarih_saat_bitis = (sorgulanan_tarih_saat_baslangic + timedelta(minutes=30)).replace(
            #     minute=int(t))
            saatin_etkinlikleri = etkinlikler.filter(Q(kort_id=kort.id) & (
                Q(baslangic_tarih_saat__lte=sorgulanan_tarih_saat_baslangic,
                  bitis_tarih_saat__gt=sorgulanan_tarih_saat_baslangic)
                # | Q(baslangic_tarih_saat__gt=sorgulanan_tarih_saat_baslangic,
                #     baslangic_tarih_saat__lt=sorgulanan_tarih_saat_bitis)
            ))
            if saatin_etkinlikleri.exists():
                etkinlikler_list = []
                for etkinlik in saatin_etkinlikleri:
                    etkinlikler_list.append({
                        "baslangic_saati": etkinlik.baslangic_tarih_saat.strftime("%H:%M"),
                        "bitis_saati": etkinlik.bitis_tarih_saat.strftime("%H:%M"),
                        "grup_adi": etkinlik.grup.__str__()[0:15],
                        "grup_id": etkinlik.grup.id,
                        "id": etkinlik.id,
                        "sure": int((etkinlik.bitis_tarih_saat - etkinlik.baslangic_tarih_saat).seconds / 60),
                        "renk": etkinlik.antrenor.renk if etkinlik.antrenor else "gray",
                        "seviye": "(" + etkinlik.top_rengi[0:1].upper() + (")" if etkinlik.top_rengi else "-"),
                        "top_rengi": etkinlik.top_rengi,
                    })
                saatler.append({"saat": str(i) + ":" + (t),
                                "etkinlikler": etkinlikler_list,
                                "bolunmeSayisi": bolunme_sayisi_getir(etkinlikler_list, kort),
                                "bekleyenVarMi": bu_saati_bekleyen_var_mi(sorgulanan_tarih_saat_baslangic, bekleyenler),
                                "sorgulananTarihSaat": sorgulanan_tarih_saat_baslangic
                                })
            else:
                saatler.append({"saat": str(i) + ":" + (t),
                                "etkinlikler": [],
                                "bolunmeSayisi": kort.max_etkinlik_sayisi,
                                "bekleyenVarMi": bu_saati_bekleyen_var_mi(sorgulanan_tarih_saat_baslangic, bekleyenler),
                                "sorgulananTarihSaat": sorgulanan_tarih_saat_baslangic
                                })
    return saatler


@login_required
def gunun_etkinlikleri_ajax(request):
    tarih = request.GET.get("tarih")
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y-%m-%d").date()
    sonraki_gun = tarih + timedelta(days=1)
    etkinlikler = EtkinlikModel.objects.filter(baslangic_tarih_saat__gte=tarih,
                                               baslangic_tarih_saat__lt=sonraki_gun).order_by(
        "-id")
    kortlar = KortModel.objects.all()
    bekleyenler = RezervasyonModel.objects.all()
    liste = []
    for kort in kortlar:
        liste.append({
            "kort_id": kort.id,
            "kort_adi": kort.adi,
            "saatler": saatler_ve_etkinlikler_dict_olustur(kort, etkinlikler, tarih, bekleyenler)
        }),
    return JsonResponse(data={"status": "success", "list": liste})


def bolunme_sayisi_getir(jsonEtkinlikler, kort):
    bolunme_sayisi = 0
    for etkinlik in jsonEtkinlikler:
        bolunme_sayisi = 5 if etkinlik["top_rengi"] == RenkEnum.K??rm??z??.value else 2
        break
    return kort.max_etkinlik_sayisi if kort.max_etkinlik_sayisi < bolunme_sayisi else bolunme_sayisi


def bu_saati_bekleyen_var_mi(tarih_saat, bekleyenler):
    gunun_saati = tarih_saat.time()
    haftanini_gunu = tarih_saat.weekday()
    gun = gunler.filter(haftanin_gunu=haftanini_gunu).first()
    saat = saatler.filter(baslangic_degeri=gunun_saati).first()
    return bekleyenler.filter(
        Q(gunler=gun, saatler=saat) |
        Q(gunler=gun, saatler__isnull=True) |
        Q(gunler__isnull=True, saatler=saat) |
        Q(gunler__isnull=True, saatler__isnull=True)).exists()


@login_required
def gunun_etkinlikleri_ajax_eski(request):
    tarih = request.GET.get("tarih")
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y-%m-%d").date()
    sonraki_gun = tarih + timedelta(days=1)
    etkinlikler = EtkinlikModel.objects.filter(baslangic_tarih_saat__gte=tarih,
                                               baslangic_tarih_saat__lt=sonraki_gun).order_by(
        "baslangic_tarih_saat")
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
                    "renk": etkinlik.antrenor.renk if etkinlik.antrenor else "gray",
                    "seviye": "(" + etkinlik.top_rengi[0:1].upper() + (")" if etkinlik.top_rengi else "-"),
                })
    return JsonResponse(data={"status": "success", "list": list})


@login_required(login_url="signup")
def getir_etkinlik_bilgisi_ajax(request):
    id = request.GET.get("id")
    event = EtkinlikModel.objects.get(id=id)
    event_dict = to_dict(event)
    return JsonResponse(event_dict)


@login_required()
def sil_etkinlik_ajax(request):
    id = request.GET.get("id")
    etklik = EtkinlikModel.objects.filter(pk=id).first()
    etklik.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


@login_required()
def sil_etkinlik(request, id):
    etklik = EtkinlikModel.objects.filter(pk=id).first()
    etklik.delete()
    messages.success(request, "Etkinlik silindi.")
    return redirect("dashboard")


@login_required
def takvim_getir(request, kort_id=None):
    kort = KortModel.objects.filter(pk=kort_id).first()
    form = EtkinlikForm()
    kortlar = KortModel.objects.all().order_by("id")
    events = EtkinlikModel.objects.filter(kort_id=kort_id) if kort_id else []
    event_list = []
    # start: '2020-09-16T16:00:00'
    for event in events:
        event_list.append(
            {
                "id": event.id,
                "title": event.grup.__str__(),
                "start": event.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "backgroundColor": event.antrenor.renk if event.antrenor else "gray",
                # "eventColor": event.renk,
            }
        )
    context = {"form": form, "etkinlikler": event_list, "kortlar": kortlar,
               "secili_kort": kort, }
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
                                          "message": "Abonelik tipi g??ncellenemez. L??tfen etkinli??i silerek yenisini olu??turunuz."})
            form = EtkinlikForm(data=request.POST, instance=eski_etkinlik)
            form.save()
        else:
            item = form.save(commit=False)
            item.user = request.user
            item.save()
        return JsonResponse(data={"status": "success", "message": "Etkinlik kaydedildi."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, EtkinlikModel)})


def etkinlik_kaydi_hata_var_mi(form):
    if form.cleaned_data["baslangic_tarih_saat"].minute % 30 != 0 or form.cleaned_data[
        "bitis_tarih_saat"].minute % 30 != 0:
        return JsonResponse(
            data={"status": "error", "message": "Etkinlik ba??lang???? ve biti?? saati 30 dakikan??n katlar?? olmal??d??r."})
    if form.cleaned_data["baslangic_tarih_saat"] > form.cleaned_data["bitis_tarih_saat"]:
        mesaj = "Etkinlik ba??lang???? tarihi biti?? tarihinden sonra olamaz."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if ayni_saatte_etkinlik_uygun_mu(form.cleaned_data["baslangic_tarih_saat"],
                                     form.cleaned_data["bitis_tarih_saat"],
                                     form.data["kort"], form.cleaned_data["pk"]):
        mesaj = "Bu kort ayn?? saat i??in maksimimum etkinlik say??s??na ula??t??."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if form.cleaned_data["abonelik_tipi"] == AbonelikTipiEnum.Paket.value:
        uyeler = paket_uyeligi_olmayan_grup_uyesi(form)
        if uyeler:
            mesaj = uyeler + " uygun paket kayd?? olmad?????? i??in etkinlik eklenemez."
            return JsonResponse(data={"status": "error", "message": mesaj})
    return False


def paket_uyeligi_olmayan_grup_uyesi(form):
    grup_id = form.data["grup" or None]
    uye_grubu = UyeGrupModel.objects.filter(grup_id=grup_id)
    grup_paketi_mi = uye_grubu.count() > 1
    uyeler = ""
    for item in uye_grubu:
        abonelik_paket_listesi = UyePaketModel.objects.filter(uye_id=item.uye_id, grup_mu=grup_paketi_mi,
                                                              aktif_mi=True)
        if not abonelik_paket_listesi.exists():
            uyeler += str(item.uye) + ", "
    if uyeler != "":
        return uyeler[:-2]
    return False


def ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, kort_id, etkinlik_id=None):
    kort = KortModel.objects.get(id=kort_id)
    result = EtkinlikModel.objects.filter(Q(kort_id=kort_id) & (
            Q(baslangic_tarih_saat__lt=baslangic_tarih_saat,
              bitis_tarih_saat__gt=baslangic_tarih_saat) |  # ba??lang???? saati herhangi bir etkinli??in i??inde olan
            Q(baslangic_tarih_saat=baslangic_tarih_saat,
              bitis_tarih_saat=bitis_tarih_saat) |  # ba??lang???? ve biti?? tarihi ayn?? olan
            Q(baslangic_tarih_saat__lt=bitis_tarih_saat, bitis_tarih_saat__gt=bitis_tarih_saat) |
            # biti?? tarihi herhangi bir etkinli??in i??inde olan
            Q(baslangic_tarih_saat__gte=baslangic_tarih_saat, bitis_tarih_saat__lte=bitis_tarih_saat))
                                          # balang???? ve biti?? saati bizim etkinli??in aras??nda olan
                                          ).exclude(id=etkinlik_id)
    return result.count() > kort.max_etkinlik_sayisi - 1


@login_required
def saat_guncelle_etkinlik_ajax(request):
    id = request.GET.get("id")
    baslangic_tarih_saat = request.GET.get("baslangic_tarih_saat")
    bitis_tarih_saat = request.GET.get("bitis_tarih_saat")
    etkinlik = EtkinlikModel.objects.filter(pk=id).first()
    if ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, etkinlik.kort_id, id):
        return JsonResponse(
            data={"status": "error", "message": "Bu kort ayn?? saat i??in maksimimum etkinlik say??s??na ula??t??."})
    etkinlik.baslangic_tarih_saat = baslangic_tarih_saat
    etkinlik.bitis_tarih_saat = bitis_tarih_saat
    etkinlik.save()
    return JsonResponse(data={"status": "success", "message": "????lem Ba??ar??l??."})


@login_required
def etkinlik_tamamlandi_ajax(request):
    "TO DO:Buras?? yetkiler tan??mland??????nda d??zenlecek. ????lemi yapan y??netici ise paket kullan??m tablosuna kay??t at??lacak."
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if etkinlik.bitis_tarih_saat > datetime.now():
            return JsonResponse(
                data={"status": "error",
                      "message": "Etkinlik biti?? saatinden ??nce tamamland?? hale getirelemez."})
        uye_grup = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
        if etkinlik.abonelik_tipi == AbonelikTipiEnum.Paket.value:
            for item in uye_grup:
                paket = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True).first()
                if paket and not PaketKullanimModel.objects.filter(uye_paket_id=paket.id,
                                                                   etkinlik_id=etkinlik.id,
                                                                   uye_id=item.uye_id).exists():
                    PaketKullanimModel.objects.create(uye_paket_id=paket.id, etkinlik_id=etkinlik.id,
                                                      uye_id=item.uye_id, user=request.user)
        etkinlik.tamamlandi_yonetici = True
        etkinlik.save()
        return JsonResponse(data={"status": "success", "message": "????lem Ba??ar??l??."})
    except Exception as e:
        return JsonResponse(data={"status": "error", "message": "Hata olu??tu." + e.__str__()})


@login_required
def etkinlik_tamamlandi_iptal_ajax(request):
    "TO DO:Buras?? yetkiler tan??mland??????nda d??zenlecek. ????lemi yapan y??netici ise paket kullan??m tablosuna kay??t at??lacak."
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        uye_grup = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
        if etkinlik.abonelik_tipi == AbonelikTipiEnum.Paket.value:
            for item in uye_grup:
                PaketKullanimModel.objects.filter(uye_id=item.uye_id, etkinlik_id=etkinlik.id).delete()
        etkinlik.tamamlandi_yonetici = False
        etkinlik.save()
        return JsonResponse(data={"status": "success", "message": "????lem Ba??ar??l??."})
    except Exception as e:
        return JsonResponse(data={"status": "error", "message": "Hata olu??tu." + e.__str__()})


# @login_required
# def katilim_ekle(request, id, uye_id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         if etkinlik.bitis_tarih_saat > datetime.now():
#             messages.error(request, "Etkinlik biti?? saatinden ??nce tamamland?? hale getirelemez.")
#             return redirect("calendarapp:profil_uye", uye_id)
#         if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id).exists():
#             EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye_id=uye_id,
#                                                 katilim_durumu=KatilimDurumuEnum.Kat??ld??.value, user=request.user)
#             # B??t??n herkes kat??l??m listesinde varsa etkinlik tamamland?? i??aretle
#             herkes_katildi_mi = True
#             for uye_grubu in etkinlik.grup.grup_uyegrup_relations.all():
#                 if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye=uye_grubu.uye).exists():
#                     herkes_katildi_mi = False
#                     break
#             if herkes_katildi_mi:
#                 etkinlik.tamamlandi_mi = True
#                 etkinlik.save()
#             messages.success(request, "????lem Ba??ar??l??.")
#         return redirect("calendarapp:profil_uye", uye_id)
#     except Exception as e:
#         messages.error(request, "Hata olu??tu." + e.__str__())
#         return redirect("calendarapp:profil_uye", uye_id)

# @login_required
# def iptal_et(request, id, uye_id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id).exists():
#             EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye_id=uye_id,
#                                                 katilim_durumu=KatilimDurumuEnum.??ptal.value, user=request.user)
#         messages.success(request, "????lem Ba??ar??l??.")
#         return redirect("calendarapp:profil_uye", uye_id)
#     except Exception as e:
#         messages.error(request, "Hata olu??tu." + e.__str__())
#         return redirect("calendarapp:profil_uye", uye_id)

# @login_required
# def iptal_et_by_antrenor(request, id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         if not EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik).exists():
#             for item in UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id):
#                 EtkinlikKatilimModel.objects.create(etkinlik=etkinlik, uye=item.uye,
#                                                     katilim_durumu=KatilimDurumuEnum.??ptal.value, user=request.user)
#         messages.success(request, "????lem Ba??ar??l??.")
#         return redirect("calendarapp:profil_antrenor", etkinlik.antrenor_id)
#     except Exception as e:
#         messages.error(request, "Hata olu??tu." + e.__str__())
#         return redirect("calendarapp:index_antrenor")

# @login_required
# def iptal_geri_al(request, id, uye_id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         iptal_edilen = EtkinlikKatilimModel.objects.filter(etkinlik=etkinlik, uye_id=uye_id,
#                                                            katilim_durumu=KatilimDurumuEnum.??ptal.value)
#         if iptal_edilen.exists():
#             iptal_edilen.delete()
#         messages.success(request, "????lem Ba??ar??l??.")
#         return redirect("calendarapp:profil_uye", uye_id)
#     except Exception as e:
#         messages.error(request, "Hata olu??tu." + e.__str__())
#         return redirect("calendarapp:profil_uye", uye_id)
#
#
# @login_required
# def iptal_geri_al_by_antrenor(request, id):
#     try:
#         etkinlik = EtkinlikModel.objects.filter(pk=id).first()
#         iptal_edilen = EtkinlikKatilimModel.objects.filter(etkinlik_id=id,
#                                                            katilim_durumu=KatilimDurumuEnum.??ptal.value)
#         if iptal_edilen.exists():
#             iptal_edilen.delete()
#         messages.success(request, "????lem Ba??ar??l??.")
#         return redirect("calendarapp:profil_antrenor", etkinlik.antrenor_id)
#     except Exception as e:
#         messages.error(request, "Hata olu??tu." + e.__str__())
#         return redirect("calendarapp:profil_antrenor")

@login_required
def etkinlik_detay_getir_ajax(request):
    etkinlik_id = request.GET.get("etkinlik_id")
    etkinlik = EtkinlikModel.objects.filter(pk=etkinlik_id).first()
    if etkinlik:
        html = render_to_string('calendarapp/etkinlik/partials/_detay_modal.html', {"etkinlik": etkinlik})
    return JsonResponse(data={"status": "success", "messages": "????lem ba??ar??l??", "html": html})

#
# def abonelik_guncelle(yeni_etkinlik_form, eski_etkinlik):
#     if yeni_etkinlik_form.cleaned_data["grup"] == eski_etkinlik.grup:  # Grup de??i??mediyse a??a????daki i??lemleri yap
#         uye_grubu = UyeGrupModel.objects.filter(grup_id=eski_etkinlik.grup_id)
#         haftaninin_gunu = eski_etkinlik.baslangic_tarih_saat.weekday()
#         for item in uye_grubu:
#             abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
#                                                        grup_id=eski_etkinlik.grup_id,
#                                                        baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat)
#             if abonelik.exists():  # Grup ??yesinin eskidende bu grubun i??indeyse zaten abonelik kayd?? vard??r. O y??zden mevcut kayd?? g??ncelle
#                 abonelik = abonelik.first()
#                 abonelik.baslangic_tarih_saat = yeni_etkinlik_form.cleaned_data["baslangic_tarih_saat"]
#                 abonelik.bitis_tarih_saat = yeni_etkinlik_form.cleaned_data["bitis_tarih_saat"]
#                 abonelik.kort = yeni_etkinlik_form.cleaned_data["kort"]
#                 haftaninin_gunu = yeni_etkinlik_form.cleaned_data["baslangic_tarih_saat"].weekday()
#                 gun_adi = gun_adi_getir(haftaninin_gunu)
#                 abonelik.gun_adi = gun_adi
#                 abonelik.save()
#             else:  # Grup ??yesinin eski tarih saatte ??yeli??i yok ise demek ki yeni gruba eklenmi??. Yeni abonelik kayd?? olu??tur.
#                 haftaninin_gunu = yeni_etkinlik_form.cleaned_data["baslangic_tarih_saat"].weekday()
#                 gun_adi = gun_adi_getir(haftaninin_gunu)
#                 UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu, gun_adi=gun_adi,
#                                                 baslangic_tarih_saat=yeni_etkinlik_form.cleaned_data[
#                                                     "baslangic_tarih_saat"],
#                                                 grup=yeni_etkinlik_form.cleaned_data["grup"],
#                                                 bitis_tarih_saat=yeni_etkinlik_form.cleaned_data["bitis_tarih_saat"],
#                                                 aktif_mi=True, kort=yeni_etkinlik_form.cleaned_data["kort"])
#     else:  # Grup de??i??tiyse eski grup ??yelerinin aboneliklerini sil, yeni ??yelere abonelik olu??tur
#         eski_uye_grubu = UyeGrupModel.objects.filter(grup_id=eski_etkinlik.grup_id)
#         yeni_uye_grubu = UyeGrupModel.objects.filter(grup_id=yeni_etkinlik_form.cleaned_data["grup"].id)
#         haftaninin_gunu = eski_etkinlik.baslangic_tarih_saat.weekday()
#         for item in eski_uye_grubu:
#             abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
#                                                        grup_id=eski_etkinlik.grup_id,
#                                                        baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat)
#             if abonelik.exists():
#                 abonelik = abonelik.first()
#                 abonelik.delete()
#         for item in yeni_uye_grubu:
#             if not UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
#                                                    baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat).exists():
#                 UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu,
#                                                 baslangic_tarih_saat=eski_etkinlik.baslangic_tarih_saat,
#                                                 grup=yeni_etkinlik_form.cleaned_data["grup"],
#                                                 bitis_tarih_saat=eski_etkinlik.bitis_tarih_saat,
#                                                 aktif_mi=True, kort=eski_etkinlik.kort)
#
#
# def abonelik_sil(etkinlik):
#     uye_grubu = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
#     haftaninin_gunu = etkinlik.baslangic_tarih_saat.weekday()
#     for item in uye_grubu:
#         abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
#                                                    baslangic_tarih_saat=etkinlik.baslangic_tarih_saat)
#         if abonelik.exists():
#             abonelik = abonelik.first()
#             abonelik.delete()
#
