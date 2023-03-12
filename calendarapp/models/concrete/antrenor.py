from django.conf import settings
from django.db import models

from calendarapp.models.Enums import AntrenorRenkEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract


class AntrenorModel(BaseAbstract):
    adi = models.CharField('Ad Soyad', max_length=250, null=False, blank=False)
    renk = models.CharField(max_length=20, choices=AntrenorRenkEnum.choices(), default="gray", verbose_name="Renk")
    ucret_katsayisi = models.DecimalField(max_digits=4, decimal_places=2, default=1.0, verbose_name="Ücret Katsayısı",
                                          null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="antrenor", null=True,
                             blank=True, verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Antrenor"
        verbose_name_plural = "Antrenor"
        ordering = ["id"]
