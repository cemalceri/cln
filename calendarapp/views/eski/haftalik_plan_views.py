from itertools import chain

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta, datetime, date, timezone
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime

from calendarapp.forms.etkinlik_forms import EtkinlikForm, HaftalikPlanForm

from calendarapp.models.Enums import KatilimDurumuEnum, AbonelikTipiEnum, GunEnum
from calendarapp.models.concrete.abonelik import UyeAbonelikModel, PaketKullanimModel, UyePaketModel
from calendarapp.models.concrete.commons import gun_adi_getir, to_dict
from calendarapp.models.concrete.etkinlik import HaftalikPlanModel, EtkinlikModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeGrupModel
from calendarapp.utils import formErrorsToText


@login_required
def haftalik_plan_getir(request, kort_id=None):
    haftalik_plan_yeni_haftaya_tasindi_kontrolu()
    kort = KortModel.objects.filter(pk=kort_id).first()
    form = HaftalikPlanForm()
    kortlar = KortModel.objects.all().order_by("id")
    event_list = []
    haftanin_plani = HaftalikPlanModel.objects.filter(kort_id=kort_id)
    for event in haftanin_plani:
        event_list.append(
            {
                "id": event.id,
                "title": event.grup.__str__(),
                "start": event.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "backgroundColor": event.antrenor.renk if event.antrenor else "gray",
            }
        )
    context = {"form": form, "etkinlikler": event_list, "kortlar": kortlar,
               "secili_kort": kort}
    return render(request, 'calendarapp/etkinlik/eski/haftalik_plan.html', context)


@login_required
def kaydet_haftalik_plan_ajax(request):
    form = HaftalikPlanForm(request.POST)
    if form.is_valid():
        result = plan_kaydi_icin_hata_var_mi(form)
        if result:
            return result
        if form.cleaned_data["pk"] and form.cleaned_data["pk"] > 0:
            eski_plan = HaftalikPlanModel.objects.get(id=form.cleaned_data["pk"])
            if form.cleaned_data["abonelik_tipi"] != eski_plan.abonelik_tipi:
                return JsonResponse(data={"status": "error",
                                          "message": "Abonelik tipi güncellenemez. Lütfen etkinliği silerek yenisini oluşturunuz."})
            abonelik_guncelle(form, eski_plan)
            form = HaftalikPlanForm(data=request.POST, instance=eski_plan)
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


@login_required(login_url="signup")
def getir_haftalik_plan_bilgisi_ajax(request):
    id = request.GET.get("id")
    event = HaftalikPlanModel.objects.get(id=id)
    event_dict = to_dict(event)
    return JsonResponse(event_dict)


@login_required
def haftalik_plan_saat_bilgisi_guncelle_ajax(request):
    id = request.GET.get("id")
    baslangic_tarih_saat = request.GET.get("baslangic_tarih_saat")
    bitis_tarih_saat = request.GET.get("bitis_tarih_saat")
    haftalik_plan = HaftalikPlanModel.objects.filter(pk=id).first()
    if ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, haftalik_plan.kort_id, id):
        return JsonResponse(
            data={"status": "error", "message": "Bu kort aynı saat için maksimimum etkinlik sayısına ulaştı."})
    haftalik_plan.baslangic_tarih_saat = baslangic_tarih_saat
    haftalik_plan.bitis_tarih_saat = bitis_tarih_saat
    haftalik_plan.save()
    haftalik_plani_takvimde_guncelle(haftalik_plan)
    return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})


@login_required()
def sil_haftalik_plan_ajax(request):
    id = request.GET.get("id")
    haftalik_plan = HaftalikPlanModel.objects.filter(pk=id).first()
    if haftalik_plan:
        abonelik_sil(haftalik_plan)
        EtkinlikModel.objects.filter(haftalik_plan_kodu=haftalik_plan.kod,
                                     baslangic_tarih_saat__gt=datetime.now()).delete()
        haftalik_plan.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


def plan_kaydi_icin_hata_var_mi(form):
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


def ayni_saatte_etkinlik_uygun_mu(baslangic_tarih_saat, bitis_tarih_saat, kort_id, etkinlik_id=None):
    kort = KortModel.objects.get(id=kort_id)
    result = HaftalikPlanModel.objects.filter(Q(kort_id=kort_id) & (
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


@login_required
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


def abonelik_sil(haftalik_plan):
    uye_grubu = UyeGrupModel.objects.filter(grup_id=haftalik_plan.grup_id)
    haftaninin_gunu = haftalik_plan.baslangic_tarih_saat.weekday()
    for item in uye_grubu:
        abonelik = UyeAbonelikModel.objects.filter(uye=item.uye, haftanin_gunu=haftaninin_gunu,
                                                   baslangic_tarih_saat=haftalik_plan.baslangic_tarih_saat)
        if abonelik.exists():
            abonelik = abonelik.first()
            abonelik.delete()


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
        plan_haftanin_gunu = parse_datetime(plan.baslangic_tarih_saat).weekday()
        for etkinlik in haftalik_plana_bagli_etkinlikler:
            etkinlik_yilin_haftasi = etkinlik.baslangic_tarih_saat.isocalendar()[1]
            yeni_baslangic_tarih_saat = datetime.now().replace(
                year=etkinlik.baslangic_tarih_saat.year, month=1, day=1, second=0, microsecond=0,
                hour=parse_datetime(plan.baslangic_tarih_saat).hour,
                minute=parse_datetime(plan.baslangic_tarih_saat).minute) + timedelta(
                days=(etkinlik_yilin_haftasi - 1) * 7) + timedelta(days=plan_haftanin_gunu + 1)
            yeni_bitis_tarih_saat = datetime.now().replace(
                year=etkinlik.bitis_tarih_saat.year, month=1, day=1, second=0, microsecond=0,
                hour=parse_datetime(plan.bitis_tarih_saat).hour,
                minute=parse_datetime(plan.bitis_tarih_saat).minute) + timedelta(
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


def haftalik_plan_yeni_haftaya_tasindi_kontrolu():
    pazartesi = datetime.now() - timedelta(days=datetime.now().weekday())
    bu_haftanini_plani = HaftalikPlanModel.objects.filter(baslangic_tarih_saat__gte=pazartesi)
    if not bu_haftanini_plani.exists():
        ilk_kayitli_plan = HaftalikPlanModel.objects.first()
        if ilk_kayitli_plan:
            aradaki_gun_sayisi = (pazartesi - ilk_kayitli_plan.baslangic_tarih_saat).days
            eklenecek_gun = 0
            islem = divmod(aradaki_gun_sayisi, 7)
            if islem[0] > 0:
                eklenecek_gun = islem[0] * 7  # Hafta Sayısı kadar gün ekle
            if islem[1] > 0:
                eklenecek_gun += 7  # kalan gün varsa bir hafta daha ekle
            for plan in HaftalikPlanModel.objects.all():
                plan.baslangic_tarih_saat += timedelta(days=eklenecek_gun)
                plan.bitis_tarih_saat += timedelta(days=eklenecek_gun)
                plan.save()
