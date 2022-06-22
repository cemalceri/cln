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
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from django.contrib import messages

from calendarapp.utils import get_verbose_name, formErrorsToText


class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/etkinlik_listesi.html"
    model = EtkinlikModel

    def get_queryset(self):
        events = EtkinlikModel.objects.getir_butun_etkinlikler(user=self.request.user)
        return events


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/etkinlik_listesi.html"
    model = EtkinlikModel

    def get_queryset(self):
        return EtkinlikModel.objects.getir_devam_eden_etkinlikler(user=self.request.user)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


# class CalendarView(LoginRequiredMixin, generic.ListView):
#     login_url = "accounts:signin"
#     model = RezervasyonModel
#     template_name = "takvim.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         d = get_date(self.request.GET.get("month", None))
#         cal = Calendar(d.year, d.month)
#         html_cal = cal.formatmonth(withyear=True)
#         context["calendar"] = mark_safe(html_cal)
#         context["prev_month"] = prev_month(d)
#         context["next_month"] = next_month(d)
#         return context


# @login_required(login_url="signup")
# def create_event(request):
#     form = RezervasyonForm(request.POST or None)
#     if request.POST and form.is_valid():
#         item = form.save(commit=False)
#         item.user = request.user
#         return HttpResponseRedirect(reverse("calendarapp:ta"))
#     print(form.errors)
#     return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = EtkinlikModel
    fields = ["Id", "title", "description", "start_time", "end_time"]
    template_name = "event.html"


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
    rezv = EtkinlikModel.objects.filter(pk=id).first()
    if rezv:
        rezv.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


@login_required(login_url="signup")
def sil_etkinlik_serisi_ajax(request):
    id = request.GET.get("id")
    etkinlik = EtkinlikModel.objects.filter(pk=id).first()
    print(etkinlik.ilk_etkinlik_id)
    etkinlik_list = EtkinlikModel.objects.filter(
        Q(pk=id) | Q(pk=etkinlik.ilk_etkinlik_id) | Q(ilk_etkinlik_id=etkinlik.ilk_etkinlik_id, ilk_etkinlik_id__isnull=False) | Q(
            ilk_etkinlik_id=id, ilk_etkinlik_id__isnull=False))
    print(etkinlik_list)
    if etkinlik_list:
        etkinlik_list.delete()
    return JsonResponse({"status": "success", "message": "Etkinlik silindi."})


@login_required
def takvim_getir(request):
    form = EtkinlikForm()
    events = EtkinlikModel.objects.getir_butun_etkinlikler()
    events_month = EtkinlikModel.objects.getir_devam_eden_etkinlikler()
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
    context = {"form": form, "events": event_list,
               "aktif_etkinlikler": events_month}
    return render(request, 'calendarapp/takvim.html', context)


@login_required
def kaydet_etkinlik_ajax(request):
    form = EtkinlikForm(request.POST)
    if form.is_valid():
        result = etkinlik_kaydi_hata_mesaji(form)
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
        return JsonResponse(data={"durum": "ok", "mesaj": "Etkinlik kaydedildi."})
    else:
        # for error in form.errors:
        return JsonResponse(data={"durum": "error", "mesaj": formErrorsToText(form.errors, EtkinlikModel)})


def etkinlik_kaydi_hata_mesaji(form):
    if form.cleaned_data["baslangic_tarih_saat"] > form.cleaned_data["bitis_tarih_saat"]:
        return JsonResponse(
            data={"durum": "error", "mesaj": "Etkinlik başlangıç tarihi bitiş tarihinden sonra olamaz."})
    elif ayni_saatte_etkinlik_var_mi(form):
        return JsonResponse(data={"durum": "error", "mesaj": "Seçilen tarih saatlerde başka etkinlik kayıtlı."})
    return False


def ayni_saatte_etkinlik_var_mi(form):
    baslangic_saat = form.cleaned_data["baslangic_tarih_saat"]
    bitis_saat = form.cleaned_data["bitis_tarih_saat"]
    result = EtkinlikModel.objects.filter(
        Q(baslangic_tarih_saat__lt=baslangic_saat, bitis_tarih_saat__gt=baslangic_saat) |
        Q(baslangic_tarih_saat__lt=bitis_saat, bitis_tarih_saat__gt=bitis_saat)).exclude(id=form.cleaned_data["pk"])
    return result.count() > 0


def etkinlik_tekrar_sayisi_kadar_ekle(request, form, etkinlik_id):
    tekrar_sayisi = form.cleaned_data["tekrar"]
    baslangic_tarih_saat = form.cleaned_data["baslangic_tarih_saat"]
    bitis_tarih_saat = form.cleaned_data["bitis_tarih_saat"]
    for i in range(tekrar_sayisi) if tekrar_sayisi and tekrar_sayisi > 0 else range(52):
        form.cleaned_data["baslangic_tarih_saat"] = baslangic_tarih_saat + timedelta(days=7 * (i + 1))
        form.cleaned_data["bitis_tarih_saat"] = bitis_tarih_saat + timedelta(days=7 * (i + 1))
        if not ayni_saatte_etkinlik_var_mi(form):
            item = EtkinlikForm(data=form.cleaned_data).save(commit=False)
            item.user = request.user
            item.ilk_etkinlik_id = etkinlik_id
            item.save()
