from django.db import models

from accounts.models import User
from calendarapp.models.Enums import GunlerModel, SaatlerModel
from calendarapp.models.abstract.base_abstract import BaseAbstract


class RezervasyonManager(models.Manager):

    def getir_butun_rezervasyonlar(self, user=None):
        events = RezervasyonModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events


class RezervasyonModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=False, blank=False)
    onem_derecesi = models.IntegerField('Önem Derecesi', null=False, blank=False, default=0)
    gunler = models.ManyToManyField(GunlerModel, verbose_name='Günler', blank=True, null=True)
    saatler = models.ManyToManyField(SaatlerModel, verbose_name='Saatler', blank=True, null=True)
    aciklama = models.TextField('Açıklama', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="rezervasyon", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    objects = RezervasyonManager()

    class Meta:
        verbose_name = "Rezervasyon"
        verbose_name_plural = "Rezervasyon"
        ordering = ["id"]

    def tercih_edilen_gunler(self):
        return " / ".join([str(i) for i in self.gunler.all()])

    def tercih_edilen_saatler(self):
        return " / ".join([str(i) for i in self.saatler.all()])

    def delete(self, *args, **kwargs):
        self.saatler.clear()
        self.gunler.clear()
        super(RezervasyonModel, self).delete(*args, **kwargs)
