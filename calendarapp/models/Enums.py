from enum import Enum

from django.db import models


class RenkEnum(Enum):
    Kırmızı = "red"
    Mavi = "blue"
    Sarı = "yellow"
    Yeşil = "green"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class GunlerModel(models.Model):
    adi = models.CharField(max_length=250, null=False, blank=False)
    haftanin_gunu = models.IntegerField(verbose_name="Haftanın Kaçıncı Günü", null=False, blank=False)
    hafta_ici_mi = models.BooleanField(verbose_name="Hafta için mi", default=False)

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Günler"
        verbose_name_plural = "Günler"
        ordering = ["id"]


class SaatlerModel(models.Model):
    adi = models.CharField(max_length=250, null=False, blank=False)
    baslangic_degeri = models.TimeField(null=False, blank=False)
    bitis_degeri = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Saatler"
        verbose_name_plural = "Saatler"
        ordering = ["id"]
