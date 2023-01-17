from django.db import models

from django.conf import settings
from calendarapp.models.Enums import SeviyeEnum, ParaHareketTuruEnum, OdemeTuruEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.uye import UyeModel


class ParaHareketiModel(BaseAbstract):
    tutar = models.DecimalField(max_length=20, verbose_name="Tutar", max_digits=10, decimal_places=2, null=False,
                                blank=False)
    hareket_turu = models.SmallIntegerField(choices=ParaHareketTuruEnum.choices(), null=True, blank=True)
    odeme_turu = models.CharField(max_length=20, null=True, blank=True)
    uye = models.ForeignKey(UyeModel, on_delete=models.SET_NULL, related_name="uye_parahareketi_relations",
                            null=True, blank=True)
    antrenor = models.ForeignKey(AntrenorModel, on_delete=models.SET_NULL,
                                 related_name="antrenor_parahareketi_relations",
                                 null=True, blank=True)
    # paket = models.ForeignKey(PaketModel, on_delete=models.SET_NULL, related_name="paket_parahareketi_relations",
    #                           null=True, blank=True)
    tarih = models.DateField(verbose_name="Tarih", null=False, blank=False)
    aciklama = models.CharField('Açıklama', max_length=250, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="user_parahareketi_relations", null=True, blank=True)

    def __str__(self):
        return self.get_hareket_turu_display() + " " + str(self.tutar)

    class Meta:
        verbose_name = "Para Hareketleri"
        verbose_name_plural = "Para Hareketleri"
        ordering = ["id"]
