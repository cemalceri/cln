from django.db import models

from django.conf import settings
from calendarapp.models.Enums import ParaHareketTuruEnum, OdemeTuruEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.abonelik import UyePaketModel
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.uye import UyeModel


class MuhasebeModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="uye_muhasebe_relations", null=True,
                            blank=True)
    yil = models.SmallIntegerField(verbose_name="Yıl", null=False, blank=False)
    ay = models.SmallIntegerField(verbose_name="Ay", null=False, blank=False)
    alacak = models.DecimalField(max_length=20, verbose_name="Alacak", max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    borc = models.DecimalField(max_length=20, verbose_name="Borç", max_digits=10, decimal_places=2, null=True,
                               blank=True)

    def __str__(self):
        return str(self.uye) + " " + str(self.yil) + " " + str(self.ay)


class ParaHareketiModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="uye_parahareketi_relations",
                            null=True, blank=True)
    hareket_turu = models.CharField(max_length=20, choices=ParaHareketTuruEnum.choices(), null=False, blank=False,
                                    default=ParaHareketTuruEnum.Borc.value)
    odeme_turu = models.CharField(max_length=20, choices=OdemeTuruEnum.choices(), null=False, blank=False,
                                  default=OdemeTuruEnum.Diger.value)
    tutar = models.DecimalField(max_length=20, verbose_name="Tutar", max_digits=10, decimal_places=2, null=False,
                                blank=False)
    tarih = models.DateField(verbose_name="Tarih", null=False, blank=False)
    aciklama = models.CharField('Açıklama', max_length=250, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name="user_parahareketi_relations", null=True, blank=True)

    def __str__(self):
        return str(self.uye) + " " + str(self.tutar) + " " + str(self.tarih)

    class Meta:
        verbose_name = "Para Hareketleri"
        verbose_name_plural = "Para Hareketleri"
        ordering = ["id"]
