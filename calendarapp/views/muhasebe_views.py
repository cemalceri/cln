from datetime import date, datetime
from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from calendarapp.forms.muhasebe_forms import UcretTarifesiKayitForm
from calendarapp.models.Enums import ParaHareketTuruEnum, UcretTuruEnum, AbonelikTipiEnum
from calendarapp.models.concrete.etkinlik import HaftalikPlanModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel, MuhasebeModel, UcretTarifesiModel
from calendarapp.models.concrete.uye import UyeGrupModel, UyeModel
from calendarapp.utils import formErrorsToText, gun_adi_ve_saati_getir


@login_required
def index(request):
    muhasebe_list = MuhasebeModel.objects.all().order_by('-id')
    return render(request, "calendarapp/muhasebe/index.html", {"muhasebe_list": muhasebe_list})


@login_required
def getir_odeme_by_id_ajax(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        odeme = ParaHareketiModel.objects.filter(pk=id).first()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "data": to_dict(odeme)})


@login_required
def index_ucret_tarifesi(request):
    form = UcretTarifesiModel.objects.all().order_by('id')
    return render(request, "calendarapp/muhasebe/ucret_tarifesi/index.html", {"list": form})


@login_required
def kaydet_ucret_tarifesi(request, id=None):
    entity = UcretTarifesiModel.objects.filter(pk=id).first()
    if request.method == 'POST':
        form = UcretTarifesiKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_ucret_tarifesi")
        else:
            messages.error(request, formErrorsToText(form.errors, UcretTarifesiModel))
            return render(request, "calendarapp/muhasebe/ucret_tarifesi/kaydet.html", context={'form': form})
    form = UcretTarifesiKayitForm(instance=entity)
    return render(request, "calendarapp/muhasebe/ucret_tarifesi/kaydet.html", context={'form': form})


@login_required
def sil_ucret_tarifesi(request, id):
    item = UcretTarifesiModel.objects.filter(pk=id).first()
    item.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_ucret_tarifesi")


@login_required
def sil_odeme(request, id):
    odeme = ParaHareketiModel.objects.filter(pk=id).first()
    uye_id = odeme.uye_id
    odeme.delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:muhasebe_uye", uye_id=uye_id)


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


@login_required
def hesapla_tum_uyelerin_borcu(request):
    uyeler = UyeModel.objects.filter(aktif_mi=True, onaylandi_mi=True)
    for uye in uyeler:
        uye_grup_ids = UyeGrupModel.objects.filter(uye_id=uye.id).values_list('grup_id', flat=True)
        uyenin_haftalik_planlari = HaftalikPlanModel.objects.filter(grup_id__in=uye_grup_ids)
        if not planlarin_ucret_bilgisi_var_mi(request, uyenin_haftalik_planlari):
            return redirect("calendarapp:index_muhasebe")
        borc_hesapla(uye.id, uyenin_haftalik_planlari)
    messages.success(request, "İşlem Başarılı.")
    return redirect("calendarapp:index_muhasebe")


@login_required
def hesapla_uye_borcu(request, uye_id):
    uye_grup_ids = UyeGrupModel.objects.filter(uye_id=uye_id).values_list('grup_id', flat=True)
    uyenin_haftalik_planlari = HaftalikPlanModel.objects.filter(grup_id__in=uye_grup_ids)
    if not planlarin_ucret_bilgisi_var_mi(request, uyenin_haftalik_planlari):
        return redirect("calendarapp:muhasebe_uye", uye_id=uye_id)
    borc_hesapla(uye_id, uyenin_haftalik_planlari)
    messages.success(request, "İşlem Başarılı.")
    return redirect("calendarapp:muhasebe_uye", uye_id=uye_id)


def borc_hesapla(uye_id, uyenin_haftalik_planlari):
    bu_yil = date.today().year
    bu_ay = date.today().month
    for plan in uyenin_haftalik_planlari:
        ucret = UcretTarifesiModel.objects.filter(seviye=plan.top_rengi, abonelik_tipi=AbonelikTipiEnum.Uyelik.name,
                                                  kisi_sayisi=plan.grup.uye_sayisi()).first().kisi_basi_ucret
        kayit = ParaHareketiModel.objects.filter(uye_id=uye_id, abonelik_id=plan.id)
        if not kayit.exists():
            aciklama = "Sistem tarafından " + gun_adi_ve_saati_getir(
                plan.baslangic_tarih_saat) + " aboneliği için otomatik olarak oluşturuldu."
            ParaHareketiModel.objects.create(uye_id=uye_id, hareket_turu=ParaHareketTuruEnum.Borc.name,
                                             ucret_turu=UcretTuruEnum.Aidat.value, tarih=date(bu_yil, bu_ay, 1),
                                             tutar=ucret, abonelik_id=plan.id, aciklama=aciklama)
        else:
            aciklama = "Sistem tarafından " + gun_adi_ve_saati_getir(
                plan.baslangic_tarih_saat) + " aboneliği için " + str(
                datetime.now().strftime("%d.%m.%Y %H:%M:%S")) + " tarihinde yeniden hesaplandı."
            kayit.update(tutar=ucret, aciklama=aciklama)


def planlarin_ucret_bilgisi_var_mi(request, planlar):
    for plan in planlar:
        if not UcretTarifesiModel.objects.filter(seviye=plan.top_rengi, abonelik_tipi=AbonelikTipiEnum.Uyelik.name,
                                                 kisi_sayisi=plan.grup.uye_sayisi()).first():
            mesaj = "Seviye: " + str(plan.top_rengi) + ", Abonelik Tipi: Üyelik, Kişi Sayısı:" + str(
                plan.grup.uye_sayisi()) + " olan ücret tarifesi bulunamadı. Ücret tarifesini ekledikten sonra tekrar deneyiniz."
            messages.error(request, mesaj)
            return False
    return True

# @login_required
# def index(request):
#     if request.method == "POST":
#         baslangic_tarihi = request.POST.get("baslangic_tarihi" or None)
#         bitis_tarihi = request.POST.get("bitis_tarihi" or None)
#         tutar_max = request.POST.get("tutar_max" or None)
#         tutar_min = request.POST.get("tutar_min" or None)
#         para_girisleri = para_haraketleri_getir(ParaHareketTuruEnum.Giris.value, baslangic_tarihi,
#                                                 bitis_tarihi, tutar_min, tutar_max)
#         para_cikislari = para_haraketleri_getir(ParaHareketTuruEnum.Cikis.value, baslangic_tarihi,
#                                                 bitis_tarihi, tutar_min, tutar_max)
#         toplam_giris = toplam_para_hareketi(para_girisleri)
#         toplam_cikis = toplam_para_hareketi(para_cikislari)
#         odeme_yapilmayan_uyelikler = son_bir_ayda_odeme_yapilmayan_uyelikler()
#         paketler = bitmek_uzere_olan_paketler()
#         filtre_metni = filtre_metni_olustur(baslangic_tarihi, bitis_tarihi, tutar_min, tutar_max)
#         context = {
#             "para_girisleri": para_girisleri,
#             "para_cikislari": para_cikislari,
#             "toplam_giris": toplam_giris,
#             "toplam_cikis": toplam_cikis,
#             "odeme_yapilmayan_uyelikler": odeme_yapilmayan_uyelikler,
#             "bitmek_uzere_olan_paketler": paketler,
#             "filtreMetni": filtre_metni
#         }
#         messages.success(request, "İşlem başarılı!")
#         return render(request, "calendarapp/muhasebe/index.html", context)
#     else:
#         para_girisleri = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Giris.value).order_by(
#             '-tarih')[0:100]
#         para_cikislari = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Cikis.value).order_by(
#             '-tarih')[0:100]
#         toplam_giris = toplam_para_hareketi(para_girisleri)
#         toplam_cikis = toplam_para_hareketi(para_cikislari)
#         odeme_yapilmayan_uyelikler = son_bir_ayda_odeme_yapilmayan_uyelikler()
#         paketler = bitmek_uzere_olan_paketler()
#         context = {
#             "para_girisleri": para_girisleri,
#             "para_cikislari": para_cikislari,
#             "toplam_giris": toplam_giris,
#             "toplam_cikis": toplam_cikis,
#             "odeme_yapilmayan_uyelikler": odeme_yapilmayan_uyelikler,
#             "bitmek_uzere_olan_paketler": paketler,
#         }
#         return render(request, "calendarapp/muhasebe/index.html", context)
#
#
# @login_required
# def kaydet_uye_odemesi_ajax(request):
#     if request.method == 'POST':
#         aciklama = request.GET.get('aciklama')
#         tarih = request.GET.get('tarih')
#         tutar = request.GET.get('tutar')
#         uye = request.GET.get('uye')
#         paket = request.GET.get('paket')
#         if tutar is None or tutar == '':
#             return JsonResponse({'status': 'error', 'message': 'Tutar boş olamaz.'})
#         if tarih is None or tarih == '':
#             return JsonResponse({'status': 'error', 'message': 'Tarih boş olamaz.'})
#         if request.GET.get('id'):
#             item = ParaHareketiModel.objects.get(id=request.POST.get('id'))
#             item.aciklama = aciklama
#             item.tarih = tarih
#             item.tutar = tutar
#             item.uye_id = uye
#             item.paket_id = paket
#             item.save()
#         else:
#             ParaHareketiModel.objects.create(paket_id=paket, aciklama=aciklama, tarih=tarih, tutar=tutar, uye_id=uye,
#                                              hareket_turu=ParaHareketTuruEnum.Giris.value)
#         return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
#
#
# @login_required
# def kaydet_antrenor_odemesi_ajax(request):
#     if request.method == 'POST':
#         aciklama = request.POST.get('aciklama')
#         tarih = request.POST.get('tarih')
#         tutar = request.POST.get('tutar')
#         anternor = request.POST.get('antrenor')
#         odeme_turu = request.POST.get('odeme_turu')
#         if tutar is None or tutar == '':
#             return JsonResponse({'status': 'error', 'message': 'Tutar boş olamaz.'})
#         if tarih is None or tarih == '':
#             return JsonResponse({'status': 'error', 'message': 'Tarih boş olamaz.'})
#         if request.POST.get('id'):
#             item = ParaHareketiModel.objects.get(id=request.POST.get('id'))
#             item.aciklama = aciklama
#             item.tarih = tarih
#             item.odeme_turu = odeme_turu
#             item.tutar = tutar
#             item.antrenor_id = anternor
#             item.save()
#         else:
#             ParaHareketiModel.objects.create(odeme_turu=odeme_turu, aciklama=aciklama, tarih=tarih, tutar=tutar,
#                                              antrenor_id=anternor, hareket_turu=ParaHareketTuruEnum.Cikis.value)
#         return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
#
#
# @login_required
# def getir_odeme_by_id_ajax(request):
#     if request.method == 'GET':
#         id = request.GET.get('id')
#         odeme = ParaHareketiModel.objects.filter(pk=id).first()
#         return JsonResponse(data={"status": "success", "message": "İşlem Başarılı.", "data": to_dict(odeme)})
#
#
# @login_required
# def sil_odeme(request, id):
#     odeme = ParaHareketiModel.objects.filter(pk=id).first()
#     uye_id = odeme.uye_id
#     odeme.delete()
#     messages.success(request, "Kayıt Silindi.")
#     return redirect("calendarapp:profil_uye", id=uye_id)
#
#
# def to_dict(instance):
#     opts = instance._meta
#     data = {}
#     for f in chain(opts.concrete_fields, opts.private_fields):
#         data[f.name] = f.value_from_object(instance)
#     for f in opts.many_to_many:
#         data[f.name] = [i.id for i in f.value_from_object(instance)]
#     return data
#
#
# def son_bir_ayda_odeme_yapilmayan_uyelikler():
#     bir_ay_onceki_gun = date.today() - timedelta(days=30)
#     son_30_odeme_idler = ParaHareketiModel.objects.filter(hareket_turu=ParaHareketTuruEnum.Giris.value,
#                                                           paket__tipi=AbonelikTipikEnum.Uyelik.value,
#                                                           tarih__gte=bir_ay_onceki_gun).values_list("paket_id",
#                                                                                                     flat=True)
#     result = UyeAbonelikModel.objects.filter(~Q(paket_id__in=son_30_odeme_idler, aktif_mi=True))
#     return result
#
#
# def para_haraketleri_getir(para_hareket_turu, baslangic_tarihi=None, bitis_tarihi=None, tutar_min=None, tutar_max=None):
#     para_hareketi = ParaHareketiModel.objects.filter(hareket_turu=para_hareket_turu)
#     if baslangic_tarihi:
#         para_hareketi = para_hareketi.filter(tarih__gte=baslangic_tarihi)
#     if bitis_tarihi:
#         para_hareketi = para_hareketi.filter(tarih__lte=bitis_tarihi)
#     if tutar_min:
#         para_hareketi = para_hareketi.filter(tutar__gte=tutar_min)
#     if tutar_max:
#         para_hareketi = para_hareketi.filter(tutar__lte=tutar_max)
#     return para_hareketi
#
#
# def toplam_para_hareketi(para_hareketi_listesi):
#     return para_hareketi_listesi.aggregate(models.Sum('tutar'))['tutar__sum']
#
#
# def filtre_metni_olustur(baslangic_tarihi=None, bitis_tarihi=None, tutar_min=None, tutar_max=None):
#     filtre_metni = ""
#     if baslangic_tarihi:
#         filtre_metni += "Başlangıç tarihi " + baslangic_tarihi + " tarihinden büyük, "
#     if bitis_tarihi:
#         filtre_metni += "Bitiş tarihi " + bitis_tarihi + " tarihinden küçük, "
#     if tutar_min:
#         filtre_metni += "Tutarı " + tutar_min + " TL'den büyük,  "
#     if tutar_max:
#         filtre_metni += "Tutarı " + tutar_max + " TL'den küçük, "
#
#     if filtre_metni == "":
#         filtre_metni = "*Filtre uygulanmadan  tüm kayıtlar gösteriliyor."
#     else:
#         filtre_metni = "*" + filtre_metni + " kayıtları gösteriliyor."
#     return filtre_metni
#
#
# def bitmek_uzere_olan_paketler():
#     paketler = PaketKullanimModel.objects.filter(kalan_adet__lte=1, kalan_adet__isnull=False).select_related(
#         "abonelik").distinct()
#     return paketler
