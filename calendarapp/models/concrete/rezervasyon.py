from datetime import datetime
from django.db import models
from django.urls import reverse
from accounts.models import User
from calendarapp.models.abstract.base_abstract import BaseAbstract


class RezervasyonManager(models.Manager):
    """ RezervasyonModel manager """

    def getir_butun_rezervasyonlar(self, user=None):
        events = RezervasyonModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events

    def getir_devam_eden_rezervasyonlar(self, user=None):
        running_events = RezervasyonModel.objects.filter(
            # user=user,
            is_active=True,
            is_deleted=False,
            bitis_tarih_saat__gte=datetime.now().date(),
        ).order_by("baslangic_tarih_saat")
        return running_events


class RezervasyonModel(BaseAbstract):
    """ RezervasyonModel model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField()
    baslangic_tarih_saat = models.DateTimeField()
    bitis_tarih_saat = models.DateTimeField()

    objects = RezervasyonManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.baslik} </a>'
