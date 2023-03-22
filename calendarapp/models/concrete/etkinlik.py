import uuid
from datetime import datetime, timedelta, time
from django.db import models
from django.urls import reverse
from django.conf import settings
from calendarapp.models.Enums import SeviyeEnum, KatilimDurumuEnum, AbonelikTipiEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeModel, GrupModel


class EtkinlikManager(models.Manager):
    """ EtkinliknModel manager """

    def getir_butun_etkinlikler(self, user=None):
        events = EtkinlikModel.objects.filter(
            iptal_mi=False,
            is_active=True, is_deleted=False)
        return events

    def getir_bugun_devam_eden_etkinlikler(self, kort_id=None, user=None):
        running_events = EtkinlikModel.objects.filter(
            iptal_mi=False,
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
            iptal_mi=False,
            is_active=True, is_deleted=False,
            baslangic_tarih_saat__lte=today_end,
            bitis_tarih_saat__gte=today_start,
        ).order_by("-baslangic_tarih_saat")
        return events

    def getir_gelecek_etkinlikler(self, user=None):
        running_events = EtkinlikModel.objects.filter(
            iptal_mi=False,
            is_active=True,
            is_deleted=False,
            bitis_tarih_saat__gte=datetime.now(),
        ).order_by("baslangic_tarih_saat")
        return running_events


class EtkinlikModel(BaseAbstract):
    haftalik_plan_kodu = models.CharField(max_length=50, null=True, blank=True)
    grup = models.ForeignKey(GrupModel, verbose_name="Katılımcı Grubu", on_delete=models.CASCADE, blank=False,
                             null=False, related_name="etkinlik_grup_relations")
    abonelik_tipi = models.CharField(max_length=20, choices=AbonelikTipiEnum.etkinlik_kaydinda_kullanilacaklar(),
                                     default=AbonelikTipiEnum.TekDers, verbose_name="Ders Tipi")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Başlangıç Tarih Saat")
    bitis_tarih_saat = models.DateTimeField(verbose_name="Bitiş Tarih Saat")
    kort = models.ForeignKey(KortModel, verbose_name="Kort", on_delete=models.CASCADE, blank=False, null=False,
                             related_name="kort")
    antrenor = models.ForeignKey(AntrenorModel, verbose_name="Antrenör", on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name="anternor")
    seviye = models.CharField(max_length=20, choices=SeviyeEnum.choices(), default="Kirmizi", null=False,
                                 blank=False, verbose_name="Top Rengi")
    tamamlandi_antrenor = models.BooleanField(default=False, verbose_name="Tamamlandı mı?")
    tamamlandi_yonetici = models.BooleanField(default=False, verbose_name="Tamamlandı mı? (Yönetici)")
    tamamlandi_uye = models.BooleanField(default=False, verbose_name="Tamamlandı mı? (Üye)")
    iptal_mi = models.BooleanField(default=False, verbose_name="İptal mi?")
    iptal_eden = models.CharField(max_length=50, null=True, blank=True)
    iptal_tarih_saat = models.DateTimeField(null=True, blank=True, verbose_name="İptal Tarih Saat")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="Açıklama")
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
    grup = models.ForeignKey(GrupModel, verbose_name="Katılımcı Grubu", on_delete=models.CASCADE, blank=False,
                             null=False, related_name="haftalikplan_grup_relations")
    abonelik_tipi = models.CharField(max_length=50, choices=AbonelikTipiEnum.haftalik_plan_kaydinda_kullanilacaklar(),
                                     default=AbonelikTipiEnum.Aidat, verbose_name="Abonelik Tipi")
    baslangic_tarih_saat = models.DateTimeField(verbose_name="Başlangıç Tarih Saat", blank=False, null=False)
    bitis_tarih_saat = models.DateTimeField(verbose_name="Bitiş Tarih Saat", blank=False, null=False)
    ders_baslangic_tarihi = models.DateField(verbose_name="İlk Ders Başlangıç Tarihi", blank=True, null=True)
    kort = models.ForeignKey(KortModel, verbose_name="Kort", on_delete=models.CASCADE, blank=False, null=False,
                             related_name="haftalikplan_kort_relations")
    antrenor = models.ForeignKey(AntrenorModel, verbose_name="Antrenör", on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name="haftalikplan_antrenor_relations")
    seviye = models.CharField(max_length=20, choices=SeviyeEnum.choices(), default="gray", null=False, blank=False,
                                 verbose_name="Top Rengi")
    aciklama = models.CharField(max_length=500, null=True, blank=True, verbose_name="Açıklama")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name="haftalikplan_user_relations", null=True,
                             blank=True, verbose_name="Ekleyen")

    class Meta:
        verbose_name = "Haftalik Plan"
        verbose_name_plural = "Haftalik Planlar"
        ordering = ["-id"]

    def __str__(self):
        return str(self.grup)
