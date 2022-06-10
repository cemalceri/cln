from django.urls import reverse
from accounts.models import User
from django.db import models
from calendarapp.models.abstract.base_abstract import BaseAbstract


class MusteriManager(models.Manager):

    def getir_butun_musteriler(self, user=None):
        events = MusteriModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events


class MusteriModel(BaseAbstract):
    """ EtkinlikModel model """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="ekleyen", null=True, blank=True,
                             verbose_name="Ekleyen")
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="Açıklama")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Başlangıç Tarih Saat")
    bitis_tarih_saat = models.DateTimeField(verbose_name="Bitiş Tarih Saat")

    objects = MusteriManager()

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ["-id"]

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.baslik} </a>'
