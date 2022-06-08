from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models.concrete.rezervasyon import RezervasyonModel


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = RezervasyonModel.objects.getir_butun_rezervasyonlar()
        running_events = RezervasyonModel.objects.getir_devam_eden_rezervasyonlar()
        latest_events = RezervasyonModel.objects.all().order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
