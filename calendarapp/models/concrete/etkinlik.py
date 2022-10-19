from datetime import datetime, timedelta, time
from django.db import models
from django.urls import reverse
from accounts.models import User
from calendarapp.models.Enums import RenkEnum, KatilimDurumuEnum
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
        ).order_by("baslangic_tarih_saat")
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
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    grup = models.ForeignKey(GrupModel, verbose_name="Katılımcı Grubu", on_delete=models.CASCADE, blank=False,
                             null=False, related_name="etkinlik_grup_relations")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Başlangıç Tarih Saat")
    bitis_tarih_saat = models.DateTimeField(verbose_name="Bitiş Tarih Saat")
    kort = models.ForeignKey(KortModel, verbose_name="Kort", on_delete=models.CASCADE, blank=False, null=False,
                             related_name="kort")
    antrenor = models.ForeignKey(AntrenorModel, verbose_name="Antrenör", on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name="anternor")
    tekrar = models.IntegerField(blank=True, null=True, verbose_name="Tekrar Sayısı")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="Açıklama")
    ilk_etkinlik_id = models.IntegerField(blank=True, null=True, verbose_name="İlk Etkinlik ID")
    tamamlandi_mi = models.BooleanField(default=False, verbose_name="Tamamlandı mı?")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="etkinlik", null=True, blank=True,
                             verbose_name="Ekleyen")

    objects = EtkinlikManager()

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ["-id"]

    def __str__(self):
        return self.baslik

    def pixel_degeri(self):
        start = self.baslangic_tarih_saat
        end = self.bitis_tarih_saat
        start_hour = start.hour
        start_minute = start.minute
        end_hour = end.hour
        end_minute = end.minute
        start_pixel = (start_hour * 60) + start_minute
        end_pixel = (end_hour * 60) + end_minute
        pixel = end_pixel - start_pixel
        return pixel

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.baslik} </a>'


class EtkinlikKatilimModel(BaseAbstract):
    etkinlik = models.ForeignKey(EtkinlikModel, verbose_name="Etkinlik", on_delete=models.CASCADE, blank=False,
                                 null=True, related_name="etkinlik")
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False,
                            related_name="uye")
    katilim_durumu = models.SmallIntegerField('Katılım Durumu', choices=KatilimDurumuEnum.choices(), null=False,
                                              blank=False, default=KatilimDurumuEnum.Katıldı.value)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="etkinlik_katilim", null=True, blank=True,
                             verbose_name="Ekleyen")

    class Meta:
        verbose_name = "Etkinlik Katılım"
        verbose_name_plural = "Etkinlik Katılımları"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.etkinlik.baslik} - {self.uye.adi}"
