# cal/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
        return RezervasyonModel.objects.getir_butun_rezervasyonlar(user=self.request.user)


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


@login_required(login_url="signup")
def create_event(request):
    form = RezervasyonForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        RezervasyonModel.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:ta"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = RezervasyonModel
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = RezervasyonModel.objects.get(id=event_id)
    eventmember = RezervasyonMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


# def add_eventmember(request, event_id):
#     forms = AddMemberForm()
#     if request.method == "POST":
#         forms = AddMemberForm(request.POST)
#         if forms.is_valid():
#             member = RezervasyonMember.objects.filter(event=event_id)
#             event = RezervasyonModel.objects.get(id=event_id)
#             if member.count() <= 9:
#                 user = forms.cleaned_data["user"]
#                 RezervasyonMember.objects.create(event=event, user=user)
#                 return redirect("calendarapp:calendar")
#             else:
#                 print("--------------User limit exceed!-----------------")
#     context = {"form": forms}
#     return render(request, "add_member.html", context)


# class EventMemberDeleteView(generic.DeleteView):
#     model = RezervasyonMember
#     template_name = "event_delete.html"
#     success_url = reverse_lazy("calendarapp:calendar")


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
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:takvim-getir")
        context = {"form": forms}
        return render(request, self.template_name, context)
