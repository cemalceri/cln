from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime

from calendarapp.forms.etkinlik_forms import HaftalikPlanForm

from calendarapp.models.Enums import AbonelikTipiEnum, SeviyeEnum
from calendarapp.models.concrete.commons import GunlerModel, SaatlerModel
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, UyePaketModel
from calendarapp.models.concrete.commons import gun_adi_getir
from calendarapp.models.concrete.etkinlik import HaftalikPlanModel, EtkinlikModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.models.concrete.uye import UyeGrupModel
from calendarapp.utils import formErrorsToText

gunler = GunlerModel.objects.all()
saatler = SaatlerModel.objects.all()


@login_required
def index(request):
    # ornek_veri_olustur()
    tarih = datetime.now().date()
    haftalik_plan_yeni_haftaya_tasindi_kontrolu()
    context = index_sayfasi_icin_context_olustur(request, tarih)
    return render(request, "calendarapp/plan/sabit_plan.html", context)


def index_sayfasi_icin_context_olustur(request, tarih):
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y/%m/%d").date()
    sorgulanan_haftanini_ilk_gunu = tarih - timedelta(days=datetime.now().weekday())
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
            html += render_to_string('calendarapp/plan/partials/_haftalik_plan_icin_kortlar.html',
                                     {'kortlar': kortlar[baslangic:bitis], 'saatler': saatler, 'tarih': gun,
                                      'tarih_str': gun.strftime("%Y-%m-%d"), 'bekleyen_listesi': bekleyen_listesi})
            baslangic += 4
            bitis += 4
        if kalan > 0:
            html += render_to_string('calendarapp/plan/partials/_haftalik_plan_icin_kortlar.html',
                                     {'kortlar': kortlar[baslangic:], 'saatler': saatler, 'tarih': gun,
                                      'tarih_str': gun.strftime("%Y-%m-%d"), 'bekleyen_listesi': bekleyen_listesi})
    context = {
        "kortlar": html,
        "haftanin_gunleri": haftanin_gunleri_strf,
    }
    return context


@login_required
def gunun_planlari_ajax(request):
    tarih = request.GET.get("tarih")
    if isinstance(tarih, str):
        tarih = datetime.strptime(tarih, "%Y-%m-%d").date()
    sonraki_gun = tarih + timedelta(days=1)
    planlar = HaftalikPlanModel.objects.filter(baslangic_tarih_saat__gte=tarih,
                                               baslangic_tarih_saat__lt=sonraki_gun).order_by("-baslangic_tarih_saat")
    liste = []
    for plan in planlar:
        liste.append({
            "id": plan.id,
            "grup": plan.grup.adi[0:5],
            "kort_id": plan.kort_id,
            "top_rengi": plan.top_rengi,
            "renk": plan.antrenor.renk if plan.antrenor else "gray",
            "baslangic_tarih_saat": plan.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M"),
            "bitis_tarih_saat": plan.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M"),
        }),
    return JsonResponse(data={"status": "success", "liste": liste})


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


@login_required()
def sil_ajax(request):
    id = request.GET.get("id")
    etkinlikleri_silinecegi_tarih = request.GET.get("etkinlikleri_silinecegi_tarih" or None)
    plan = HaftalikPlanModel.objects.filter(pk=id).first()
    if plan:
        abonelik_sil(plan)
        if etkinlikleri_silinecegi_tarih:
            tarih = datetime.strptime(etkinlikleri_silinecegi_tarih, "%Y-%m-%d").date()
            EtkinlikModel.objects.filter(haftalik_plan_kodu=plan.kod,
                                         baslangic_tarih_saat__gt=tarih).delete()
        else:
            EtkinlikModel.objects.filter(haftalik_plan_kodu=plan.kod, baslangic_tarih_saat__gt=datetime.now()).delete()
        plan.delete()
    return JsonResponse({"status": "success", "message": "İşlem başarılı."})


def abonelik_sil(plan):
    uye_grubu = UyeGrupModel.objects.filter(grup_id=plan.grup_id)
    haftaninin_gunu = plan.baslangic_tarih_saat.weekday()
    for item in uye_grubu:
        abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                   baslangic_tarih_saat=plan.baslangic_tarih_saat)
        if abonelik.exists():
            abonelik = abonelik.first()
            abonelik.delete()


@login_required
def kaydet_ajax(request):
    form = HaftalikPlanForm(request.GET)
    if form.is_valid():
        result = plan_kaydi_icin_hata_var_mi(form)
        if result:
            return result
        if form.cleaned_data["pk"] and form.cleaned_data["pk"] > 0:
            eski_plan = HaftalikPlanModel.objects.get(id=form.cleaned_data["pk"])
            if form.cleaned_data["abonelik_tipi"] != eski_plan.abonelik_tipi:
                return JsonResponse(data={"status": "error",
                                          "message": "Abonelik tipi güncellenemez. Lütfen kaydı silerek yenisini oluşturunuz."})
            abonelik_guncelle(form, eski_plan)
            form = HaftalikPlanForm(data=request.GET, instance=eski_plan)
            plan = form.save()
            haftalik_plani_takvimde_guncelle(plan)
        else:
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            abonelik_olustur(plan)
            haftalik_plani_takvimde_guncelle(plan)
        return JsonResponse(data={"status": "success", "message": "Kayıt Edildi."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, HaftalikPlanModel)})


@login_required
def kaydet_modal_ajax(request):
    kort_id = request.GET.get("kort_id")
    baslangic_tarih_saat = request.GET.get("baslangic_tarih_saat")
    bitis_tarih_saat = parse_datetime(baslangic_tarih_saat) + timedelta(minutes=30)
    form = HaftalikPlanForm(initial={"kort": kort_id, "baslangic_tarih_saat": baslangic_tarih_saat,
                                     "bitis_tarih_saat": bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M")})
    html = render_to_string("calendarapp/plan/partials/_plan_kaydet_modal.html", {"form": form})
    return JsonResponse(data={"status": "success", "html": html})


@login_required
def duzenle_modal_ajax(request):
    id = request.GET.get("id")
    plan = HaftalikPlanModel.objects.filter(pk=id).first()
    form = HaftalikPlanForm(instance=plan)
    html = render_to_string("calendarapp/plan/partials/_plan_kaydet_modal.html", {"form": form})
    return JsonResponse(data={"status": "success", "html": html})


@login_required
def detay_modal_ajax(request):
    plan_id = request.GET.get("plan_id")
    item = HaftalikPlanModel.objects.filter(pk=plan_id).first()
    if item:
        html = render_to_string('calendarapp/plan/partials/_plan_detay_modal.html', {"etkinlik": item})
    return JsonResponse(data={"status": "success", "messages": "İşlem başarılı", "html": html})


def grup_uyesinin_bu_saatte_plan_var_mi(id, baslangic_tarih_saat, grup):
    if HaftalikPlanModel.objects.filter(grup=grup, baslangic_tarih_saat=baslangic_tarih_saat).exclude(pk=id).exists():
        return "Bu saat aynı üye/grup için zaten kayıtlı. "
    grup_uyeleri = UyeGrupModel.objects.filter(grup=grup)
    # for item in grup_uyeleri:
    #     if UyeAbonelikModel.objects.filter(uye=item.uye, baslangic_tarih_saat=baslangic_tarih_saat).exists():
    #         return "Grupta bulunan " + str(item.uye) + " üyesinin bu saatte abonelik kaydı var."
    return None


def plan_kaydi_icin_hata_var_mi(form):
    if form.cleaned_data["baslangic_tarih_saat"] > form.cleaned_data["bitis_tarih_saat"] or form.cleaned_data[
        "baslangic_tarih_saat"] == form.cleaned_data["bitis_tarih_saat"]:
        mesaj = "Başlangıç tarihi bitiş tarihi uygun değil."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if form.cleaned_data["baslangic_tarih_saat"].minute % 30 != 0 or form.cleaned_data[
        "bitis_tarih_saat"].minute % 30 != 0:
        mesaj = "Başlangıç ve bitiş saati 30 dakikanın katları olmalıdır."
        return JsonResponse(data={"status": "error", "message": mesaj})
    if ayni_saatte_plan_uygun_mu(form.cleaned_data["baslangic_tarih_saat"], form.cleaned_data["bitis_tarih_saat"],
                                 form.data["kort"], form.cleaned_data["top_rengi"], form.cleaned_data["pk"]) is False:
        mesaj = "Bu saatte kayıtlı olan diğer etkinlikler için bu top rengi uygun değil."
        return JsonResponse(data={"status": "error", "message": mesaj})
    uyelik_var_mi = grup_uyesinin_bu_saatte_plan_var_mi(form.cleaned_data["pk"],
                                                        form.cleaned_data["baslangic_tarih_saat"],
                                                        form.cleaned_data["grup"])
    if uyelik_var_mi:
        return JsonResponse(data={"status": "error", "message": uyelik_var_mi})
    if form.cleaned_data["abonelik_tipi"] == AbonelikTipiEnum.Paket.value:
        uyeler = paket_uyeligi_olmayan_grup_uyesi(form)
        if uyeler:
            mesaj = uyeler + " paket kaydı olmadığı için kayıt eklenemez."
            return JsonResponse(data={"status": "error", "message": mesaj})
    return False


def abonelik_olustur(haftalik_plan):
    uye_grubu = UyeGrupModel.objects.filter(grup_id=haftalik_plan.grup_id)
    haftaninin_gunu = haftalik_plan.baslangic_tarih_saat.weekday()
    gun_adi = gun_adi_getir(haftaninin_gunu)
    for item in uye_grubu:
        if not UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                               baslangic_tarih_saat=haftalik_plan.baslangic_tarih_saat).exists():
            UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu, gun_adi=gun_adi,
                                            baslangic_tarih_saat=haftalik_plan.baslangic_tarih_saat,
                                            grup=haftalik_plan.grup,
                                            bitis_tarih_saat=haftalik_plan.bitis_tarih_saat,
                                            aktif_mi=True, kort=haftalik_plan.kort, user=haftalik_plan.user)


def abonelik_guncelle(yeni_haftalik_plan_form, eski_haftalik_plan):
    if yeni_haftalik_plan_form.cleaned_data[
        "grup"] == eski_haftalik_plan.grup:  # Grup değişmediyse aşağıdaki işlemleri yap
        uye_grubu = UyeGrupModel.objects.filter(grup_id=eski_haftalik_plan.grup_id)
        haftaninin_gunu = eski_haftalik_plan.baslangic_tarih_saat.weekday()
        for item in uye_grubu:
            abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                       grup_id=eski_haftalik_plan.grup_id,
                                                       baslangic_tarih_saat=eski_haftalik_plan.baslangic_tarih_saat)
            if abonelik.exists():  # Grup üyesinin eskidende bu grubun içindeyse zaten abonelik kaydı vardır. O yüzden mevcut kaydı güncelle
                abonelik = abonelik.first()
                abonelik.baslangic_tarih_saat = yeni_haftalik_plan_form.cleaned_data["baslangic_tarih_saat"]
                abonelik.bitis_tarih_saat = yeni_haftalik_plan_form.cleaned_data["bitis_tarih_saat"]
                abonelik.kort = yeni_haftalik_plan_form.cleaned_data["kort"]
                haftaninin_gunu = yeni_haftalik_plan_form.cleaned_data["baslangic_tarih_saat"].weekday()
                gun_adi = gun_adi_getir(haftaninin_gunu)
                abonelik.gun_adi = gun_adi
                abonelik.save()
            else:  # Grup üyesinin eski tarih saatte üyeliği yok ise demek ki yeni gruba eklenmiş. Yeni abonelik kaydı oluştur.
                haftaninin_gunu = yeni_haftalik_plan_form.cleaned_data["baslangic_tarih_saat"].weekday()
                gun_adi = gun_adi_getir(haftaninin_gunu)
                UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu, gun_adi=gun_adi,
                                                baslangic_tarih_saat=yeni_haftalik_plan_form.cleaned_data[
                                                    "baslangic_tarih_saat"],
                                                grup=yeni_haftalik_plan_form.cleaned_data["grup"],
                                                bitis_tarih_saat=yeni_haftalik_plan_form.cleaned_data[
                                                    "bitis_tarih_saat"],
                                                aktif_mi=True, kort=yeni_haftalik_plan_form.cleaned_data["kort"])
    else:  # Grup değiştiyse eski grup üyelerinin aboneliklerini sil, yeni üyelere abonelik oluştur
        eski_uye_grubu = UyeGrupModel.objects.filter(grup_id=eski_haftalik_plan.grup_id)
        yeni_uye_grubu = UyeGrupModel.objects.filter(grup_id=yeni_haftalik_plan_form.cleaned_data["grup"].id)
        haftaninin_gunu = eski_haftalik_plan.baslangic_tarih_saat.weekday()
        for item in eski_uye_grubu:
            abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                       grup_id=eski_haftalik_plan.grup_id,
                                                       baslangic_tarih_saat=eski_haftalik_plan.baslangic_tarih_saat)
            if abonelik.exists():
                abonelik = abonelik.first()
                abonelik.delete()
        for item in yeni_uye_grubu:
            if not UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                   baslangic_tarih_saat=eski_haftalik_plan.baslangic_tarih_saat).exists():
                UyeAbonelikModel.objects.create(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                baslangic_tarih_saat=eski_haftalik_plan.baslangic_tarih_saat,
                                                grup=yeni_haftalik_plan_form.cleaned_data["grup"],
                                                bitis_tarih_saat=eski_haftalik_plan.bitis_tarih_saat,
                                                aktif_mi=True, kort=eski_haftalik_plan.kort)


def haftalik_plani_takvimde_guncelle(plan):
    haftalik_plana_bagli_etkinlikler = EtkinlikModel.objects.filter(haftalik_plan_kodu=plan.kod)
    if not haftalik_plana_bagli_etkinlikler.exists():  # Haftalık plana bağlı etkinlik yoksa oluştur
        baslangic_tarih_saat = plan.baslangic_tarih_saat
        if isinstance(plan.baslangic_tarih_saat, str):
            baslangic_tarih_saat = datetime.strptime(plan.baslangic_tarih_saat, "%Y-%m-%dT%H:%M:%S")
        if baslangic_tarih_saat > datetime.now():
            EtkinlikModel.objects.create(haftalik_plan_kodu=plan.kod, grup=plan.grup,
                                         abonelik_tipi=plan.abonelik_tipi,
                                         baslangic_tarih_saat=plan.baslangic_tarih_saat,
                                         bitis_tarih_saat=plan.bitis_tarih_saat, kort=plan.kort,
                                         antrenor=plan.antrenor,
                                         top_rengi=plan.top_rengi, aciklama=plan.aciklama)
    else:  # Haftalık plana bağlı etkinli varsa güncelle
        plan_haftanin_gunu = plan.baslangic_tarih_saat.weekday()
        for etkinlik in haftalik_plana_bagli_etkinlikler:
            etkinlik_yilin_haftasi = etkinlik.baslangic_tarih_saat.isocalendar()[1]
            yeni_baslangic_tarih_saat = datetime.now().replace(
                year=etkinlik.baslangic_tarih_saat.year, month=1, day=1, second=0, microsecond=0,
                hour=plan.baslangic_tarih_saat.hour, minute=plan.baslangic_tarih_saat.minute) + timedelta(
                days=(etkinlik_yilin_haftasi - 1) * 7) + timedelta(days=plan_haftanin_gunu + 1)
            yeni_bitis_tarih_saat = datetime.now().replace(
                year=etkinlik.bitis_tarih_saat.year, month=1, day=1, second=0, microsecond=0,
                hour=plan.bitis_tarih_saat.hour, minute=plan.bitis_tarih_saat.minute) + timedelta(
                days=(etkinlik_yilin_haftasi - 1) * 7) + timedelta(days=plan_haftanin_gunu + 1)
            if yeni_baslangic_tarih_saat > datetime.now():  # bugünden sonrakilerin gün ve saat değişikliğini etkinliğe uygula
                etkinlik.grup = plan.grup
                etkinlik.abonelik_tipi = plan.abonelik_tipi
                etkinlik.kort = plan.kort
                etkinlik.baslangic_tarih_saat = yeni_baslangic_tarih_saat
                etkinlik.bitis_tarih_saat = yeni_bitis_tarih_saat
                etkinlik.antrenor = plan.antrenor
                etkinlik.top_rengi = plan.top_rengi
                etkinlik.aciklama = plan.aciklama
                etkinlik.save()


def ayni_saatte_plan_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, kort_id, top_rengi, plan_id=None):
    planlar = HaftalikPlanModel.objects.filter(Q(kort_id=kort_id) & (
        # başlangıç saati herhangi bir etkinliğin içinde olan
            Q(baslangic_tarih_saat__lt=baslangic_tarih_saat, bitis_tarih_saat__gt=baslangic_tarih_saat) |
            # veya başlangıç ve bitiş tarihi aynı olan
            Q(baslangic_tarih_saat=baslangic_tarih_saat, bitis_tarih_saat=bitis_tarih_saat) |
            # veya bitiş tarihi herhangi bir etkinliğin içinde olan
            Q(baslangic_tarih_saat__lt=bitis_tarih_saat, bitis_tarih_saat__gt=bitis_tarih_saat) |
            # veya balangıç ve bitiş saati bizim etkinliğin arasında olan
            Q(baslangic_tarih_saat__gte=baslangic_tarih_saat, bitis_tarih_saat__lte=bitis_tarih_saat))).exclude(
        id=plan_id)
    result = True
    if planlar.filter(top_rengi=SeviyeEnum.Kirmizi).exists() and (
            top_rengi != SeviyeEnum.Kirmizi.name or top_rengi != SeviyeEnum.TenisOkulu.name):
        result = False
    if planlar.filter(top_rengi=SeviyeEnum.TenisOkulu).exists() and (
            top_rengi != SeviyeEnum.Kirmizi.name or top_rengi != SeviyeEnum.Kirmizi.name):
        result = False
    if top_rengi == SeviyeEnum.Yetiskin.name and planlar.exists():
        result = False
    if ((
            top_rengi == SeviyeEnum.Turuncu.name or top_rengi == SeviyeEnum.Sari.name or top_rengi == SeviyeEnum.Yesil.name)
            and (planlar.filter(top_rengi=SeviyeEnum.Kirmizi).exists()
                 or planlar.filter(top_rengi=SeviyeEnum.TenisOkulu).exists()
                 or planlar.filter(top_rengi=SeviyeEnum.Yetiskin).exists())):
        result = False
    return result


def paket_uyeligi_olmayan_grup_uyesi(form):
    grup_id = form.data["grup" or None]
    uye_grubu = UyeGrupModel.objects.filter(grup_id=grup_id)
    uyeler = ""
    grup_paketi_mi = uye_grubu.count() > 1
    for item in uye_grubu:
        abonelik_paket_listesi = UyePaketModel.objects.filter(uye_id=item.uye_id, aktif_mi=True, grup_mu=grup_paketi_mi)
        if not abonelik_paket_listesi.exists():
            uyeler += str(item.uye) + ", "
    if uyeler != "":
        return uyeler[:-2]
    return False


def haftalik_plan_yeni_haftaya_tasindi_kontrolu():
    bu_haftaninin_pazartesi = datetime.now() - timedelta(days=datetime.now().weekday())
    onceki_haftalarin_plani = HaftalikPlanModel.objects.filter(baslangic_tarih_saat__lt=bu_haftaninin_pazartesi)
    # Bu haftanın öncesindeki planların haftalık planlar tablosundaki tarihlerini güncelle
    if onceki_haftalarin_plani.exists():
        for plan in onceki_haftalarin_plani:
            plan_pazartesi = plan.baslangic_tarih_saat - timedelta(days=plan.baslangic_tarih_saat.weekday())
            fark = (bu_haftaninin_pazartesi - plan_pazartesi).days
            plan.baslangic_tarih_saat += timedelta(days=fark)
            plan.bitis_tarih_saat += timedelta(days=fark)
            plan.save()


def ornek_veri_olustur():
    gun = datetime.now() - timedelta(days=datetime.now().weekday()),
    for t in range(0, 7):
        for i in range(9, 23):
            for kort in KortModel.objects.all():
                baslangic_tarih_saat = datetime(gun[0].year, gun[0].month, gun[0].day, i, 0, 0)
                bitis_tarih_saat = datetime(gun[0].year, gun[0].month, gun[0].day, i + 1, 0, 0)
                HaftalikPlanModel.objects.create(abonelik_tipi="Uyelik", top_rengi="Kirmizi", antrenor_id=1, grup_id=7,
                                                 kort_id=kort.id,
                                                 user_id=1, baslangic_tarih_saat=baslangic_tarih_saat,
                                                 bitis_tarih_saat=bitis_tarih_saat, aciklama="Test")
        gun = (gun[0] + timedelta(days=1),)
