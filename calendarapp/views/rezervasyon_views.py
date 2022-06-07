# cal/views.py
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from calendarapp.models.member.rezervasyon_member import RezervasyonMember
from calendarapp.forms.rezervasyon_forms import RezervasyonForm
from django.views.generic import ListView
from calendarapp.models.concrete.rezervasyon import RezervasyonModel


class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/rezervasyon_listesi.html"
    model = RezervasyonModel

    def get_queryset(self):
        events = RezervasyonModel.objects.getir_butun_rezervasyonlar(user=self.request.user)
        return events


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/rezervasyon_listesi.html"
    model = RezervasyonModel

    def get_queryset(self):
        return RezervasyonModel.objects.getir_devam_eden_rezervasyonlar(user=self.request.user)


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
    model = RezervasyonModel
    fields = ["Id", "title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def getir_rezervasyon_bilgisi_ajax(request):
    id = request.GET.get("id")
    event = RezervasyonModel.objects.get(id=id)
    event_dict = model_to_dict(event)
    return JsonResponse(event_dict)


@login_required(login_url="signup")
def sil_rezervasyon_ajax(request):
    id = request.GET.get("id")
    rezv = RezervasyonModel.objects.filter(pk=id).first()
    if rezv:
        rezv.delete()
    return JsonResponse({"data": "success"})


class TakvimView(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/takvim.html"
    form_class = RezervasyonForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = RezervasyonModel.objects.getir_butun_rezervasyonlar(user=request.user)
        events_month = RezervasyonModel.objects.getir_devam_eden_rezervasyonlar(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "id": event.id,
                    "title": event.baslik,
                    "start": event.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        context = {"form": forms, "events": event_list,
                   "aktif_rezervasyonlar": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            if forms.cleaned_data["pk"] > 0:
                form = RezervasyonForm(data=request.POST,
                                       instance=RezervasyonModel.objects.get(id=forms.cleaned_data["pk"]))
                form.save()
                return redirect("calendarapp:takvim-getir")
            form = forms.create_(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:takvim-getir")
        context = {"form": forms}
        return render(request, self.template_name, context)


@login_required
def takvim_getir(request):
    form = RezervasyonForm()
    events = RezervasyonModel.objects.getir_butun_rezervasyonlar()
    events_month = RezervasyonModel.objects.getir_devam_eden_rezervasyonlar()
    event_list = []
    # start: '2020-09-16T16:00:00'
    for event in events:
        event_list.append(
            {
                "id": event.id,
                "title": event.baslik,
                "start": event.baslangic_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.bitis_tarih_saat.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )
    context = {"form": form, "events": event_list,
               "aktif_rezervasyonlar": events_month}
    return render(request, 'calendarapp/takvim.html', context)


@login_required
def kaydet_rezervasyon_ajax(request):
    form = RezervasyonForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data["pk"])
        if form.cleaned_data["pk"] and form.cleaned_data["pk"] > 0:
            form = RezervasyonForm(data=request.POST,
                                   instance=RezervasyonModel.objects.get(id=form.cleaned_data["pk"]))
            form.save()
            return redirect("calendarapp:takvim-getir")
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return redirect("calendarapp:takvim-getir")
    else:
        print(form.errors)
    context = {"form": form}
    return render(request, 'calendarapp/takvim.html', context)
