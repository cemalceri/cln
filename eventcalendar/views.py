from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models.concrete.etkinlik import EtkinlikModel


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = EtkinlikModel.objects.getir_butun_etkinlikler()
        running_events = EtkinlikModel.objects.getir_devam_eden_etkinlikler()
        latest_events = EtkinlikModel.objects.all().order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
