from datetime import datetime

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models.concrete.etkinlik import EtkinlikModel


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        tum_etkinlik_sayisi = EtkinlikModel.objects.filter(is_active=True, is_deleted=False).count()
        bugun_kalan_etkinlik_sayisi = EtkinlikModel.objects.getir_bugun_devam_eden_etkinlikler().count()
        gelecek_etkinlikler = EtkinlikModel.objects.getir_gelecek_etkinlikler()

        context = {
            "tum_etkinlik_sayisi": tum_etkinlik_sayisi,
            "bugun_kalan_etkinlik_sayisi": bugun_kalan_etkinlik_sayisi,
            "gelecek_etkinlikler": gelecek_etkinlikler,
        }
        return render(request, self.template_name, context)
