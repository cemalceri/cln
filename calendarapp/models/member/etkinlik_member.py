from django.db import models

from accounts.models import User
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.etkinlik import EtkinlikModel


class EtkinlikMember(BaseAbstract):
    """ EtkinlikModel member model """

    etkinlik = models.ForeignKey(EtkinlikModel, on_delete=models.CASCADE, related_name="etkinlik")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_members")

    class Meta:
        unique_together = ["etkinlik", "user"]

    def __str__(self):
        return str(self.user)
