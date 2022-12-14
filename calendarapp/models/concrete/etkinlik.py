import uuid
from datetime import datetime, timedelta, time
from django.db import models
from django.urls import reverse
from django.conf import settings
from calendarapp.models.Enums import RenkEnum, KatilimDurumuEnum, AbonelikTipiEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeModel, GrupModel


class EtkinlikManager(models.Manager):
    """ EtkinliknModel manager """

    def getir_butun_etkinlikler(self, user=None):
        events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events

    def getir_bugun_devam_eden_etkinlikler(self, kort_id=None, user=None):
        running_events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True,
            is_deleted=False,
            baslangic_tarih_saat__day=datetime.now().day,
            bitis_tarih_saat__gte=datetime.now(),
            kort_id=kort_id,
        ).order_by("baslangic_tarih_saat")
        return running_events

    def getir_bugunun_etkinlikleri(self, user=None):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False,
            baslangic_tarih_saat__lte=today_end,
            bitis_tarih_saat__gte=today_start,
        ).order_by("-baslangic_tarih_saat")
        return events

    def getir_gelecek_etkinlikler(self, user=None):
        running_events = EtkinlikModel.objects.filter(
            # user=user,
            is_active=True,
            is_deleted=False,
            bitis_tarih_saat__gte=datetime.now(),
        ).order_by("baslangic_tarih_saat")
        return running_events


class EtkinlikModel(BaseAbstract):
    haftalik_plan_kodu = models.CharField(max_length=50, null=True, blank=True)
    grup = models.ForeignKey(GrupModel, verbose_name="Kat??l??mc?? Grubu", on_delete=models.CASCADE, blank=False,
                             null=False, related_name="etkinlik_grup_relations")
    abonelik_tipi = models.IntegerField(choices=AbonelikTipiEnum.choices(), default=2, verbose_name="Abonelik Tipi")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Ba??lang???? Tarih Saat")
    bitis_tarih_saat = models.DateTimeField(verbose_name="Biti?? Tarih Saat")
    kort = models.ForeignKey(KortModel, verbose_name="Kort", on_delete=models.CASCADE, blank=False, null=False,
                             related_name="kort")
    antrenor = models.ForeignKey(AntrenorModel, verbose_name="Antren??r", on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name="anternor")
    top_rengi = models.CharField(max_length=20, choices=RenkEnum.choices(), default="gray", null=False, blank=False,
                                 verbose_name="Top Rengi")
    tamamlandi_antrenor = models.BooleanField(default=False, verbose_name="Tamamland?? m???")
    tamamlandi_yonetici = models.BooleanField(default=False, verbose_name="Tamamland?? m??? (Y??netici)")
    tamamlandi_uye = models.BooleanField(default=False, verbose_name="Tamamland?? m??? (??ye)")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="A????klama")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="etkinlik", null=True,
                             blank=True,
                             verbose_name="Ekleyen")

    objects = EtkinlikManager()

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ["-id"]

    def __str__(self):
        return str(self.grup)

    def pixel_degeri(self):
        # start = self.baslangic_tarih_saat
        # end = self.bitis_tarih_saat
        # start_hour = start.hour
        # start_minute = start.minute
        # end_hour = end.hour
        # end_minute = end.minute
        # start_pixel = (start_hour * 60) + start_minute
        # end_pixel = (end_hour * 60) + end_minute
        # pixel = end_pixel - start_pixel
        # print((self.baslangic_tarih_saat -).total_seconds() / 60)
        pixel = (self.bitis_tarih_saat - self.baslangic_tarih_saat).total_seconds() / 60
        # print(self.baslangic_tarih_saat, self.bitis_tarih_saat, pixel)
        return int(pixel)

    # def ayni_gun_kendinden_onceki_etkinlik_ile_arasindaki_dakika(self):
    #     today = datetime.now().date()
    #     gecen_dakika = 0
    #     today_start = datetime.combine(today, time()) + timedelta(minutes=540)
    #     gunun_etkinlikleri = EtkinlikModel.objects.filter(kort_id=self.kort_id,
    #                                                       bitis_tarih_saat__gte=today_start).order_by(
    #         "baslangic_tarih_saat")
    #     if gunun_etkinlikleri.first().id == self.id:
    #         gecen_dakika = (self.baslangic_tarih_saat - today_start).total_seconds() / 60
    #     else:
    #         start = self.baslangic_tarih_saat
    #         onceki_etkinlik = EtkinlikModel.objects.filter(kort_id=self.kort_id,
    #                                                        bitis_tarih_saat__gte=today_start,
    #                                                        baslangic_tarih_saat__lt=start).order_by(
    #             "-baslangic_tarih_saat").first()
    #         if onceki_etkinlik:
    #             onceki_etkinlik_bitis = onceki_etkinlik.bitis_tarih_saat
    #             gecen_dakika = (start - onceki_etkinlik_bitis).seconds / 60
    #     return int(gecen_dakika)

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id))

    def renk(self):
        if self.antrenor:
            return self.antrenor.renk
        else:
            return "white"

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.baslik} </a>'


def generate_uuid():
    return uuid.uuid4()

class HaftalikPlanModel(BaseAbstract):
    kod = models.UUIDField(primary_key=False, verbose_name="Plan Kodu", default=generate_uuid, editable=False)
    grup = models.ForeignKey(GrupModel, verbose_name="Kat??l??mc?? Grubu", on_delete=models.CASCADE, blank=False,
                             null=False, related_name="haftalikplan_grup_relations")
    abonelik_tipi = models.IntegerField(choices=AbonelikTipiEnum.choices(), default=2, verbose_name="Abonelik Tipi")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Ba??lang???? Tarih Saat", blank=False, null=False)
    bitis_tarih_saat = models.DateTimeField(verbose_name="Biti?? Tarih Saat", blank=False, null=False)
    kort = models.ForeignKey(KortModel, verbose_name="Kort", on_delete=models.CASCADE, blank=False, null=False,
                             related_name="haftalikplan_kort_relations")
    antrenor = models.ForeignKey(AntrenorModel, verbose_name="Antren??r", on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name="haftalikplan_antrenor_relations")
    top_rengi = models.CharField(max_length=20, choices=RenkEnum.choices(), default="gray", null=False, blank=False,
                                 verbose_name="Top Rengi")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="A????klama")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name="haftalikplan_user_relations", null=True,
                             blank=True, verbose_name="Ekleyen")

    class Meta:
        verbose_name = "Haftalik Plan"
        verbose_name_plural = "Haftalik Planlar"
        ordering = ["-id"]

    def __str__(self):
        return str(self.grup)


