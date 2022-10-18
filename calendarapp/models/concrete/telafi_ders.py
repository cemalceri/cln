from django.db import models

from accounts.models import User
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.uye import UyeModel


class TelafiDersModel(BaseAbstract):
    telafi_etkinlik = models.ForeignKey(EtkinlikModel, on_delete=models.CASCADE, related_name="telafiDers",
                                        verbose_name="Etkinlik", null=False, blank=False)
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="telafiDers", verbose_name="Üye",
                            null=False, blank=False)
    yapilan_kort = models.ForeignKey("KortModel", on_delete=models.CASCADE, related_name="telafi_ders_kort",
                                        null=True,
                                        blank=True)
    yapilan_antrenor = models.ForeignKey(AntrenorModel, on_delete=models.CASCADE,
                                            related_name="telafi_ders_antrenor", null=True, blank=True)
    yapilma_tarih_saat = models.DateTimeField(verbose_name="Etkinlik Tarihi", null=True, blank=True)
    yapilma_aciklama = models.TextField(verbose_name="Etkinlik Açıklaması", null=True, blank=True)
    aciklama = models.TextField('Açıklama', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="telafiDers", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.uye.adi + " " + self.uye.soyadi

    class Meta:
        verbose_name = "Antrenor"
        verbose_name_plural = "Antrenor"
        ordering = ["id"]
