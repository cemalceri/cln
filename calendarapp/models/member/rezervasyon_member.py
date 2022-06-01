from django.db import models

from accounts.models import User
from calendarapp.models.abstract.rezervasyon_abstract import RezervasyonAbstract
from calendarapp.models.concrete.rezervasyon import RezervasyonModel


class RezervasyonMember(RezervasyonAbstract):
    """ RezervasyonModel member model """

    rezevasyon = models.ForeignKey(RezervasyonModel, on_delete=models.CASCADE, related_name="rezevasyon")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_members")

    class Meta:
        unique_together = ["rezevasyon", "user"]

    def __str__(self):
        return str(self.user)
