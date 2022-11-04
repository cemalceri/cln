from django.conf import settings
from django.db import models


from calendarapp.models.Enums import RenkEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract


class AntrenorModel(BaseAbstract):
    adi = models.CharField('Ad Soyad', max_length=250, null=False, blank=False)
    renk = models.CharField(max_length=20, choices=RenkEnum.choices(), default="purple",
                            verbose_name="Renk")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="antrenor", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Antrenor"
        verbose_name_plural = "Antrenor"
        ordering = ["id"]
