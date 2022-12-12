from itertools import chain

from django.db import models

from django.conf import settings
from calendarapp.models.abstract.base_abstract import BaseAbstract


class OkulModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="okul", null=True,
                             blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Okul"
        verbose_name_plural = "Okul"
        ordering = ["id"]


def gun_adi_getir(haftanin_gunu):
    if haftanin_gunu == 0:
        return "Pazartesi"
    elif haftanin_gunu == 1:
        return "Salı"
    elif haftanin_gunu == 2:
        return "Çarşamba"
    elif haftanin_gunu == 3:
        return "Perşembe"
    elif haftanin_gunu == 4:
        return "Cuma"
    elif haftanin_gunu == 5:
        return "Cumartesi"
    elif haftanin_gunu == 6:
        return "Pazar"


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data
