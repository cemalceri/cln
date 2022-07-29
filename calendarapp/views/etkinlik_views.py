# cal/views.py
from itertools import chain

from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import generic
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from calendarapp.forms.etkinlik_forms import EtkinlikForm
from django.views.generic import ListView
from calendarapp.models.concrete.etkinlik import EtkinlikModel, EtkinlikKatilimModel
from django.contrib import messages

from calendarapp.models.concrete.kort import KortModel
from calendarapp.utils import get_verbose_name, formErrorsToText


class ButunEtkinliklerListView(ListView):
    template_name = "calendarapp/etkinlik/etkinlik_listesi.html"
    model = EtkinlikModel

    def get_queryset(self):
        events = EtkinlikModel.objects.getir_butun_etkinlikler(user=self.request.user)
        return events


class BugunEtkinlikleriListView(ListView):
    template_name = "calendarapp/etkinlik/etkinlik_listesi.html"
    model = EtkinlikModel

    def get_queryset(self):
        return EtkinlikModel.objects.getir_bugunun_etkinlikleri()


class GelecekEtkinliklerListView(ListView):
    template_name = "calendarapp/etkinlik/etkinlik_listesi.html"
    model = EtkinlikModel

    def get_queryset(self):
        return EtkinlikModel.objects.getir_gelecek_etkinlikler()


# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split("-"))
#         return date(year, month, day=1)
#     return datetime.today()
#
#
# def prev_month(d):
#     first = d.replace(day=1)
#     prev_month = first - timedelta(days=1)
#     month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
#     return month
#
#
# def next_month(d):
#     days_in_month = calendar.monthrange(d.year, d.month)[1]
#     last = d.replace(day=days_in_month)
#     next_month = last + timedelta(days=1)
#     month = "month=" + str(next_month.year) + "-" + str(next_month.month)
#     return month
#

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
                "title": event.baslik,
                "start": event.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "backgroundColor": event.renk,
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
            form = EtkinlikForm(data=request.POST,
                                instance=EtkinlikModel.objects.get(id=form.cleaned_data["pk"]))
            form.save()
        else:
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            etkinlik_tekrar_sayisi_kadar_ekle(request, form, item.id)
        return JsonResponse(data={"status": "success", "message": "Etkinlik kaydedildi."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, EtkinlikModel)})


def etkinlik_kaydi_hata_var_mi(form):
    mesaj = None
    if form.cleaned_data["baslangic_tarih_saat"] > form.cleaned_data["bitis_tarih_saat"]:
        mesaj = "Etkinlik başlangıç tarihi bitiş tarihinden sonra olamaz."
    elif ayni_saatte_etkinlik_uygun_mu(form.cleaned_data["baslangic_tarih_saat"], form.cleaned_data["bitis_tarih_saat"],
                                       form.data["kort"], form.cleaned_data["pk"]):
        mesaj = "Seçilen tarih saate başka etkinlik eklenemez."
    if mesaj is not None:
        return JsonResponse(data={"status": "error", "message": mesaj})
    return False


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


def etkinlik_tekrar_sayisi_kadar_ekle(request, form, etkinlik_id):
    tekrar_sayisi = form.cleaned_data["tekrar"]
    baslangic_tarih_saat = form.cleaned_data["baslangic_tarih_saat"]
    bitis_tarih_saat = form.cleaned_data["bitis_tarih_saat"]
    if tekrar_sayisi and tekrar_sayisi > 0:
        for i in range(tekrar_sayisi):
            form.cleaned_data["baslangic_tarih_saat"] = baslangic_tarih_saat + timedelta(days=7 * (i + 1))
            form.cleaned_data["bitis_tarih_saat"] = bitis_tarih_saat + timedelta(days=7 * (i + 1))
            if not ayni_saatte_etkinlik_uygun_mu(form.cleaned_data["baslangic_tarih_saat"],
                                                 form.cleaned_data["bitis_tarih_saat"], form.data["kort"]):
                item = EtkinlikForm(data=form.cleaned_data).save(commit=False)
                item.user = request.user
                item.ilk_etkinlik_id = etkinlik_id
                item.save()


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
    return JsonResponse(data={"status": "success", "message": "Etkinlik guncellendi."})


@login_required
def etkinlik_tamamlandi_ajax(request):
    try:
        id = request.GET.get("id")
        etkinlik = EtkinlikModel.objects.filter(pk=id).first()
        if etkinlik.bitis_tarih_saat > datetime.now():
            return JsonResponse(
                data={"status": "error", "message": "Etkinlik bitiş saatinden önce tamamlandı hale getirelemez."})
        etkinlik.tamamlandi_mi = True
        etkinlik.save()
        if etkinlik.grup.uye1:
            EtkinlikKatilimModel.objects.create(etkinlik_id=etkinlik.id, uye=etkinlik.grup.uye1, user=request.user)
        if etkinlik.grup.uye2:
            EtkinlikKatilimModel.objects.create(etkinlik_id=etkinlik.id, uye=etkinlik.grup.uye2, user=request.user)
        if etkinlik.grup.uye3:
            EtkinlikKatilimModel.objects.create(etkinlik_id=etkinlik.id, uye=etkinlik.grup.uye3, user=request.user)
        if etkinlik.grup.uye4:
            EtkinlikKatilimModel.objects.create(etkinlik_id=etkinlik.id, uye=etkinlik.grup.uye4, user=request.user)
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
    except Exception as e:
        return JsonResponse(data={"status": "error", "message": "Hata oluştu." + e.__str__()})
