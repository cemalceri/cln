from django.db import models
from django.conf import settings
from calendarapp.models.abstract.base_abstract import BaseAbstract


class KortManager(models.Manager):
    def getir_butun_kortlar(self, user=None):
        events = KortModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events


class KortModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="kort", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    objects = KortManager()

    class Meta:
        verbose_name = "Kort"
        verbose_name_plural = "Kort"
        ordering = ["id"]
