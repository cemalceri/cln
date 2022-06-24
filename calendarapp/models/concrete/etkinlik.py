from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from accounts.models import User
from calendarapp.models.Enums import RenkEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel


class EtkinlikManager(models.Manager):
    """ EtkinliknModel manager """

    def getir_butun_etkinlikler(self, user=None):
        events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events

    def getir_bugun_devam_eden_etkinlikler(self, user=None):
        running_events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True,
            is_deleted=False,
            bitis_tarih_saat__gte=datetime.now(),
            bitis_tarih_saat__lt=(datetime.now() + timedelta(days=1)),
        ).order_by("baslangic_tarih_saat")
        return running_events

    def getir_gelecek_etkinlikler(self, user=None):
        running_events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True,
            is_deleted=False,
            bitis_tarih_saat__gte=datetime.now(),
        ).order_by("baslangic_tarih_saat")
        return running_events


class EtkinlikModel(BaseAbstract):
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    grup = models.ForeignKey(UyeGrupModel, verbose_name="Katılımcı Grubu", on_delete=models.CASCADE, blank=False,
                             null=True, related_name="grup")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Başlangıç Tarih Saat")
    bitis_tarih_saat = models.DateTimeField(verbose_name="Bitiş Tarih Saat")
    renk = models.CharField(max_length=20, choices=RenkEnum.choices(), default="gray",
                            verbose_name="Renk")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="Açıklama")
    tekrar = models.IntegerField(blank=True, null=True, verbose_name="Tekrar Sayısı")
    ilk_etkinlik_id = models.IntegerField(blank=True, null=True, verbose_name="İlk Etkinlik ID")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="events", null=True, blank=True,
                             verbose_name="Ekleyen")

    objects = EtkinlikManager()

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ["-id"]

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.baslik} </a>'
