from django.db import models

from django.conf import settings

from calendarapp.models.Enums import SeviyeEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.commons import GunlerModel, SaatlerModel
from calendarapp.models.concrete.uye import UyeModel


class RezervasyonManager(models.Manager):

    def getir_butun_rezervasyonlar(self, user=None):
        events = RezervasyonModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events


class RezervasyonModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="rezervasyonlar", verbose_name="Üye",
                            null=True, blank=True)
    misafir = models.CharField(max_length=100, verbose_name="Misafir", null=True, blank=True)
    seviye = models.CharField('Seviye', max_length=20, choices=SeviyeEnum.choices(), null=False,
                                    blank=False, default="red")
    onem_derecesi = models.IntegerField('Önem Derecesi', null=True, blank=True, default=0)
    referans = models.CharField('Referans', max_length=100, null=True, blank=True)
    gunler = models.ManyToManyField(GunlerModel, verbose_name='Günler', blank=True, null=True,
                                    related_name='gunler_rezervasyon_tablosu')
    saatler = models.ManyToManyField(SaatlerModel, verbose_name='Saatler', blank=True, null=True,
                                     related_name='saatler_rezervasyon_tablosu')
    antrenor = models.ForeignKey(AntrenorModel, on_delete=models.SET_NULL, related_name="antrenor", null=True,
                                 blank=True)
    aktif_mi = models.BooleanField('Aktif Mi', default=True)
    aciklama = models.TextField('Açıklama', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="rezervasyon", null=True,
                             blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        if self.uye:
            return self.uye.adi + " " + self.uye.soyadi
        else:
            return self.misafir

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
