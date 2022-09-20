from django.db import models

from accounts.models import User
from calendarapp.models.abstract.base_abstract import BaseAbstract


class OkulModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="okul", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Okul"
        verbose_name_plural = "Okul"
        ordering = ["id"]
