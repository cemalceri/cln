from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime, parse_date

from calendarapp.forms.etkinlik_forms import EtkinlikForm

from calendarapp.models.Enums import AbonelikTipiEnum, SeviyeEnum
from calendarapp.models.concrete.abonelik import PaketKullanimModel, UyePaketModel
from calendarapp.models.concrete.commons import to_dict, GunlerModel, SaatlerModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel, HaftalikPlanModel
from django.contrib import messages

from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.muhasebe import UcretTarifesiModel
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel
from calendarapp.models.concrete.uye import UyeGrupModel
from calendarapp.utils import formErrorsToText

gunler = GunlerModel.objects.all()
saatler = SaatlerModel.objects.all()


@login_required
def index(request):
    tarih = datetime.now().date()
    context = index_sayfasi_icin_context_olustur(request, tarih)
    return render(request, "calendarapp/etkinlik/haftalik_etkinlikler.html", context)


@login_required
def index_getir_by_tarih(request, tarih):
    tarih = tarih.replace(".", "/")
    context = index_sayfasi_icin_context_olustur(request, tarih)
    return render(request, "calendarapp/etkinlik/haftalik_etkinlikler.html", context)


def index_sayfasi_icin_context_olustur(request, tarih):
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y/%m/%d").date()
    sorgulanan_haftanini_ilk_gunu = tarih - timedelta(days=tarih.weekday())
    haftanin_gunleri = []
    haftanin_gunleri_strf = []
    kortlar = KortModel.objects.all().order_by("id")
    for i in range(0, 7):
        haftanin_gunleri.append(sorgulanan_haftanini_ilk_gunu + timedelta(days=i))
        haftanin_gunleri_strf.append((sorgulanan_haftanini_ilk_gunu + timedelta(days=i)).strftime("%Y-%m-%d"))
    saatler = []
    dakikalar = ["00", "30"]
    for i in range(8, 24):
        for dk in dakikalar:
            if len(str(i)) == 1:
                saatler.append({
                    "saat": "0" + str(i) + ":" + dk,
                    "saat_for_id": "0" + str(i) + "-" + dk
                })
            else:
                saatler.append({
                    "saat": str(i) + ":" + dk,
                    "saat_for_id": str(i) + "-" + dk
                })
    bekleyen_listesi = []
    for bekleyen in RezervasyonModel.objects.filter(aktif_mi=True):
        for gunler in bekleyen.gunler.all():
            for saat in bekleyen.saatler.all():
                bekleyen_listesi.append({
                    "id": saat.baslangic_degeri.strftime("%H-%M") + "_" + gunler.adi
                })
    bekleyen_listesi = [dict(t) for t in {tuple(d.items()) for d in bekleyen_listesi}]  # remove same record
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
                                      'tarih_str': gun.strftime("%Y-%m-%d"), 'bekleyen_listesi': bekleyen_listesi})
            baslangic += 4
            bitis += 4
        if kalan > 0:
            html += render_to_string('calendarapp/etkinlik/partials/_gunluk_plan_icin_kortlar.html',
                                     {'kortlar': kortlar[baslangic:], 'saatler': saatler, 'tarih': gun,
                                      'tarih_str': gun.strftime("%Y-%m-%d"), 'bekleyen_listesi': bekleyen_listesi})
    context = {
        "kortlar": html,
        "haftanin_gunleri": haftanin_gunleri_strf,
        "sorgulanan_tarih": tarih,
    }
    return context


@login_required
def gunun_etkinlikleri_ajax(request):
    tarih = request.GET.get("tarih")
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y-%m-%d").date()
    sonraki_gun = tarih + timedelta(days=1)
    planlar = EtkinlikModel.objects.filter(baslangic_tarih_saat__gte=tarih, iptal_mi=False,
                                           baslangic_tarih_saat__lt=sonraki_gun).order_by("-baslangic_tarih_saat")
    liste = []
    for plan in planlar:
        liste.append({
            "id": plan.id,
            "grup": plan.grup.adi[0:5],
            "kort_id": plan.kort_id,
            "seviye": plan.seviye,
            "renk": plan.antrenor.renk if plan.antrenor else "gray",
            "baslangic_tarih_saat": plan.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M"),
            "bitis_tarih_saat": plan.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M"),
        }),
    return JsonResponse(data={"status": "success", "liste": liste})


@login_required
def gunun_etkinlikleri_ajax_eski(request):
    tarih = request.GET.get("tarih")
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y-%m-%d").date()
    sonraki_gun = tarih + timedelta(days=1)
    etkinlikler = EtkinlikModel.objects.filter(baslangic_tarih_saat__gte=tarih, iptal_mi=False,
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
                    "seviye": "(" + etkinlik.seviye[0:1].upper() + (")" if etkinlik.seviye else "-"),
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
    sonrakiler_silinsin_mi = request.GET.get("sonrakiler_silinsin_mi")
    etkinlik = EtkinlikModel.objects.filter(pk=id).first()
    if sonrakiler_silinsin_mi == "true" and etkinlik.haftalik_plan_kodu:
        EtkinlikModel.objects.filter(haftalik_plan_kodu=etkinlik.haftalik_plan_kodu, iptal_mi=False,
                                     baslangic_tarih_saat__gte=etkinlik.baslangic_tarih_saat).delete()
    etkinlik.delete()
    UyePaketModel.objects.filter(etkinlik_id=id).delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


@login_required()
def sil_etkinlik(request, id):
    etkinlik = EtkinlikModel.objects.filter(pk=id).first()
    etkinlik.delete()
    messages.success(request, "Etkinlik silindi.")
    return redirect("dashboard")


@login_required
def kaydet_etkinlik_ajax(request):
    form = EtkinlikForm(request.GET)
    if form.is_valid():
        result = etkinlik_kaydi_hata_var_mi(form)
        if result:
            return result
        if form.cleaned_data["pk"] and form.cleaned_data["pk"] > 0:
            eski_etkinlik = EtkinlikModel.objects.get(id=form.cleaned_data["pk"])
            form = EtkinlikForm(data=request.GET, instance=eski_etkinlik)
            item = form.save()
        else:
            item = form.save(commit=False)
            item.user = request.user
            item.save()
        uyelere_paket_ekle_veya_guncelle(item)
        return JsonResponse(data={"status": "success", "message": "Etkinlik kaydedildi."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, EtkinlikModel)})


def etkinlik_kaydi_hata_var_mi(form):
    if ayni_saatte_etkinlik_uygun_mu(form.cleaned_data["baslangic_tarih_saat"], form.cleaned_data["bitis_tarih_saat"],
                                     form.data["kort"], form.cleaned_data["seviye"],
                                     form.cleaned_data["pk"]) is False:
        mesaj = "Bu saatte kayıtlı olan diğer kayıtlar için bu top rengi uygun değil."
        return JsonResponse(data={"status": "error", "message": mesaj})
    telafi_dersi_olmayan_grup = telafi_dersi_grup_uyeleri_getir(form)
    if form.cleaned_data["abonelik_tipi"] == AbonelikTipiEnum.Telafi.name and telafi_dersi_olmayan_grup:
        mesaj = telafi_dersi_olmayan_grup + " üye/üyelerinin telafi hakkı bulunmamaktadır."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if ucret_tarifesi_var_mi(form.cleaned_data["seviye"], form.cleaned_data["abonelik_tipi"],
                             form.data["grup"]) is False:
        mesaj = "Lütfen ücret tarifesi menüsünden ücret bilgisini ekleyiniz."
        return JsonResponse(data={"status": "error", "message": mesaj})


def ucret_tarifesi_var_mi(seviye, abonelik_tipi, grup_id):
    if abonelik_tipi == AbonelikTipiEnum.Telafi.name:
        return True
    kisi_sayisi = UyeGrupModel.objects.filter(grup_id=grup_id).count()
    tarife = UcretTarifesiModel.objects.filter(seviye=seviye, abonelik_tipi=abonelik_tipi,
                                               kisi_sayisi=kisi_sayisi)
    return tarife.exists()


def uyelere_paket_ekle_veya_guncelle(etkinlik):
    uye_grubu = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
    ucret_tarifesi = UcretTarifesiModel.objects.filter(seviye=etkinlik.seviye,
                                                       abonelik_tipi=etkinlik.abonelik_tipi,
                                                       kisi_sayisi=uye_grubu.count()).first()
    if ucret_tarifesi:
        grup_mu = True if uye_grubu.count() > 1 else False
        for item in uye_grubu:
            paket = UyePaketModel.objects.filter(uye=item.uye, etkinlik_id=etkinlik.id)
            if not paket.exists():
                UyePaketModel.objects.create(ucret_tarifesi=ucret_tarifesi, uye=item.uye, grup_mu=grup_mu,
                                             baslangic_tarih=etkinlik.baslangic_tarih_saat.date(),
                                             bitis_tarih=etkinlik.bitis_tarih_saat.date(),
                                             adet=1, etkinlik_id=etkinlik.id)
            else:
                paket = paket.first()
                paket.ucret_tarifesi = ucret_tarifesi
                paket.uye = item.uye
                paket.grup_mu = grup_mu
                paket.baslangic_tarih = etkinlik.baslangic_tarih_saat.date()
                paket.bitis_tarih = etkinlik.bitis_tarih_saat.date()
                paket.adet = 1
                paket.aktif_mi = True
                paket.save()
    else: # ücret tarifesi yoksa telefi ders olarak güncellenmiştir. Çünkü kayıt öncesinde ücret tarifesi olup olmadığı kontrol edilmiştir.
        UyePaketModel.objects.filter(etkinlik_id=etkinlik.id).delete()



def ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, kort_id, seviye, etkinlik_id=None):
    planlar = EtkinlikModel.objects.filter(Q(kort_id=kort_id, iptal_mi=False) & (
        # başlangıç saati herhangi bir etkinliğin içinde olan
            Q(baslangic_tarih_saat__lt=baslangic_tarih_saat, bitis_tarih_saat__gt=baslangic_tarih_saat) |
            # veya başlangıç ve bitiş tarihi aynı olan
            Q(baslangic_tarih_saat=baslangic_tarih_saat, bitis_tarih_saat=bitis_tarih_saat) |
            # veya bitiş tarihi herhangi bir etkinliğin içinde olan
            Q(baslangic_tarih_saat__lt=bitis_tarih_saat, bitis_tarih_saat__gt=bitis_tarih_saat) |
            # veya balangıç ve bitiş saati bizim etkinliğin arasında olan
            Q(baslangic_tarih_saat__gte=baslangic_tarih_saat, bitis_tarih_saat__lte=bitis_tarih_saat))).exclude(
        id=etkinlik_id)
    result = True
    if planlar.filter(seviye=SeviyeEnum.Kirmizi).exists() and (
            seviye != SeviyeEnum.Kirmizi.name or seviye != SeviyeEnum.TenisOkulu.name):
        result = False
    if planlar.filter(seviye=SeviyeEnum.TenisOkulu).exists() and (
            seviye != SeviyeEnum.Kirmizi.name or seviye != SeviyeEnum.Kirmizi.name):
        result = False
    if seviye == SeviyeEnum.Yetiskin.name and planlar.exists():
        result = False
    if ((
            seviye == SeviyeEnum.Turuncu.name or seviye == SeviyeEnum.Sari.name or seviye == SeviyeEnum.Yesil.name)
            and (planlar.filter(seviye=SeviyeEnum.Kirmizi).exists()
                 or planlar.filter(seviye=SeviyeEnum.TenisOkulu).exists()
                 or planlar.filter(seviye=SeviyeEnum.Yetiskin).exists())):
        result = False
    return result


def paketi_olmayan_grup_uyeleri_getir(form):
    grup_id = form.data["grup" or None]
    uye_grubu = UyeGrupModel.objects.filter(grup_id=grup_id)
    uyeler = ""
    grup_paketi_mi = uye_grubu.count() > 1
    for item in uye_grubu:
        abonelik_paket_listesi = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True, grup_mu=grup_paketi_mi,
                                                              ucret_tarifesi__abonelik_tipi=form.cleaned_data[
                                                                  "abonelik_tipi"])
        if not abonelik_paket_listesi.exists():
            uyeler += str(item.uye) + ", "
    if uyeler != "":
        return uyeler[:-2]
    return None


def telafi_dersi_grup_uyeleri_getir(form):
    grup_id = form.data["grup" or None]
    uye_grubu = UyeGrupModel.objects.filter(grup_id=grup_id)
    uyeler = ""
    for item in uye_grubu:
        telafi_ders = TelafiDersModel.objects.filter(uye_id=item.uye_id)
        if not telafi_ders.exists():
            uyeler += str(item.uye) + ", "
    if uyeler != "":
        return uyeler[:-2]
    return None


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
    """TO DO:Burası yetkiler tanımlandığında düzenlecek. İşlemi yapan yönetici ise paket kullanım tablosuna kayıt atılacak."""
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if etkinlik.bitis_tarih_saat > datetime.now():
            return JsonResponse(
                data={"status": "error",
                      "message": "Etkinlik bitiş saatinden önce tamamlandı hale getirelemez."})
        uye_grup = UyeGrupModel.objects.filter(grup_id=etkinlik.grup_id)
        grup_mu = uye_grup.count() > 1
        for item in uye_grup:
            paket = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True, grup_mu=grup_mu,
                                                 ucret_tarifesi__abonelik_tipi=etkinlik.abonelik_tipi).first()
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
def tamamlandi_iptal_ajax(request):
    """TO DO:Burası yetkiler tanımlandığında düzenlecek. İşlemi yapan yönetici ise paket kullanım tablosuna kayıt atılacak."""
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


@login_required
def detay_modal_ajax(request):
    etkinlik_id = request.GET.get("etkinlik_id")
    etkinlik = EtkinlikModel.objects.filter(pk=etkinlik_id).first()
    if etkinlik:
        html = render_to_string('calendarapp/etkinlik/partials/_etkinlik_detay_modal.html', {"etkinlik": etkinlik})
    return JsonResponse(data={"status": "success", "messages": "İşlem başarılı", "html": html})


@login_required
def kaydet_modal_ajax(request):
    kort_id = request.GET.get("kort_id")
    baslangic_tarih_saat = request.GET.get("baslangic_tarih_saat")
    bitis_tarih_saat = parse_datetime(baslangic_tarih_saat) + timedelta(minutes=30)
    form = EtkinlikForm(initial={"kort": kort_id, "baslangic_tarih_saat": baslangic_tarih_saat,
                                 "bitis_tarih_saat": bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M")})
    html = render_to_string("calendarapp/etkinlik/partials/_etkinlik_kaydet_modal.html", {"form": form})
    return JsonResponse(data={"status": "success", "html": html})


@login_required
def duzenle_modal_ajax(request):
    etkinlik_id = request.GET.get("etkinlik_id")
    etkinlik = EtkinlikModel.objects.filter(pk=etkinlik_id).first()
    form = EtkinlikForm(instance=etkinlik)
    html = render_to_string("calendarapp/etkinlik/partials/_etkinlik_kaydet_modal.html", {"form": form})
    return JsonResponse(data={"status": "success", "html": html})


@login_required
def haftayi_sabit_plandan_olustur_ajax(request):
    tarih = request.GET.get("tarih")
    tarih = datetime.strptime(tarih, "%Y/%m/%d").date()
    pazartesi = tarih - timedelta(days=tarih.weekday())
    if pazartesi < datetime.now().date():
        return JsonResponse(data={"status": "error", "message": "Geçmiş tarihler için işlem yapılamaz."})
    sabit_planlar = HaftalikPlanModel.objects.all().order_by("baslangic_tarih_saat")
    gun_farki = (pazartesi - sabit_planlar.first().baslangic_tarih_saat.date()).days
    for plan in sabit_planlar:
        if plan.ders_baslangic_tarihi:
            kayda_baslanacak_tarih = plan.baslangic_tarih_saat.date() + timedelta(days=gun_farki)
            tarih_kontrolu = True if kayda_baslanacak_tarih >= plan.ders_baslangic_tarihi else False
        else:
            tarih_kontrolu = True
        if not EtkinlikModel.objects.filter(haftalik_plan_kodu=plan.kod, grup=plan.grup, iptal_mi=False,
                                            baslangic_tarih_saat=plan.baslangic_tarih_saat + timedelta(days=gun_farki),
                                            ).exists() and tarih_kontrolu:  # Belirlenen günden önce etkinlik tablosuna otomatik kayıt oluşturulmaması için
            EtkinlikModel.objects.create(haftalik_plan_kodu=plan.kod, grup=plan.grup,
                                         abonelik_tipi=plan.abonelik_tipi,
                                         baslangic_tarih_saat=plan.baslangic_tarih_saat + timedelta(days=gun_farki),
                                         bitis_tarih_saat=plan.bitis_tarih_saat + timedelta(days=gun_farki),
                                         kort=plan.kort,
                                         antrenor=plan.antrenor, seviye=plan.seviye, aciklama=plan.aciklama)
    return JsonResponse(data={"status": "success", "message": "İşlem başarılı."})


@login_required
def haftanin_etkinliklerini_sil_ajax(request):
    tarih = request.GET.get("tarih")
    tarih = datetime.strptime(tarih, "%Y/%m/%d").date()
    pazartesi = tarih - timedelta(days=tarih.weekday())
    if pazartesi < datetime.now().date():
        return JsonResponse(data={"status": "error", "message": "Geçmiş tarihler için işlem yapılamaz."})
    haftanin_etkinlikleri = EtkinlikModel.objects.filter(baslangic_tarih_saat__gte=pazartesi, iptal_mi=False,
                                                         haftalik_plan_kodu__isnull=False,
                                                         baslangic_tarih_saat__lt=pazartesi + timedelta(days=7))

    if haftanin_etkinlikleri.exists():
        haftanin_etkinlikleri.delete()
        return JsonResponse(data={"status": "success", "message": "İşlem başarılı."})
    return JsonResponse(data={"status": "error", "message": "Bu haftada kayıtlı etkinlik yok."})
