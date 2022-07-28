from django.db import models

from accounts.models import User
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.uye import UyeModel


class TelafiDersModel(BaseAbstract):
    telafi_etkinlik = models.ForeignKey(EtkinlikModel, on_delete=models.CASCADE, related_name="telafiDers",
                                        verbose_name="Etkinlik")
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="telafiDers", verbose_name="Üye")
    kullanilan_etkinlik = models.ForeignKey(EtkinlikModel, on_delete=models.CASCADE, related_name="kullanilanDers",
                                            verbose_name="Kullanılan Etkinlik")
    aciklama = models.TextField('Açıklama', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="antrenor", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Antrenor"
        verbose_name_plural = "Antrenor"
        ordering = ["id"]