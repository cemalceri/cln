from django.db import models

from django.conf import settings
from django.db.models import Sum

from calendarapp.models.Enums import ParaHareketTuruEnum, SeviyeEnum, AbonelikTipiEnum, UcretTuruEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.uye import UyeModel


class MuhasebeModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="uye_muhasebe_relations", null=True,
                            blank=True)
    yil = models.SmallIntegerField(verbose_name="Yıl", null=False, blank=False)
    ay = models.SmallIntegerField(verbose_name="Ay", null=False, blank=False)
    odeme = models.DecimalField(max_length=20, verbose_name="Alacak", max_digits=10, decimal_places=2, null=True,
                                blank=True)
    borc = models.DecimalField(max_length=20, verbose_name="Borç", max_digits=10, decimal_places=2, null=True,
                               blank=True)

    def __str__(self):
        return str(self.uye) + " " + str(self.yil) + " " + str(self.ay)

    @property
    def toplam_aylik_borc(self):
        borc_toplami = \
            ParaHareketiModel.objects.filter(uye_id=self.uye.id, hareket_turu=ParaHareketTuruEnum.Borc.name,
                                             tarih__year=self.yil, tarih__month=self.ay).aggregate(
                Sum('tutar'))['tutar__sum']
        self.borc = borc_toplami
        self.save()
        return borc_toplami if borc_toplami else 0

    @property
    def toplam_aylik_odeme(self):
        odeme_toplami = \
            ParaHareketiModel.objects.filter(uye_id=self.uye.id, hareket_turu=ParaHareketTuruEnum.Odeme.name,
                                             tarih__year=self.yil, tarih__month=self.ay).aggregate(
                Sum('tutar'))['tutar__sum']
        self.odeme = odeme_toplami
        self.save()
        return odeme_toplami if odeme_toplami else 0

    def fark(self):
        return self.toplam_aylik_odeme - self.toplam_aylik_borc

    def hesapla_butonu_gosterilecek_mi(self):
        from datetime import datetime
        if self.yil == datetime.now().year and self.ay == datetime.now().month:
            return True
        else:
            return False

    def toplam_odeme(self):
        return \
            ParaHareketiModel.objects.filter(uye_id=self.uye.id, hareket_turu=ParaHareketTuruEnum.Odeme.name).aggregate(
                Sum('tutar'))['tutar__sum'] or 0

    def toplam_borc(self):
        return \
            ParaHareketiModel.objects.filter(uye_id=self.uye.id, hareket_turu=ParaHareketTuruEnum.Borc.name).aggregate(
                Sum('tutar'))['tutar__sum'] or 0

    def toplam_fark(self):
        return self.toplam_odeme() - self.toplam_borc()


class ParaHareketiModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, related_name="uye_parahareketi_relations",
                            null=True, blank=True, verbose_name="Üye")
    hareket_turu = models.CharField(max_length=20, choices=ParaHareketTuruEnum.choices(), null=False, blank=False,
                                    default=ParaHareketTuruEnum.Borc.value)
    ucret_turu = models.CharField("Türü", max_length=20, choices=UcretTuruEnum.choices(), null=False, blank=False,
                                  default=UcretTuruEnum.Diger.value)
    tutar = models.DecimalField(max_length=20, verbose_name="Tutar", max_digits=10, decimal_places=2, null=False,
                                blank=False)
    tarih = models.DateField(verbose_name="Tarih", null=False, blank=False)
    paket = models.ForeignKey('UyePaketModel', on_delete=models.CASCADE, related_name="paket_parahareketi_relations",
                              null=True, blank=True)
    abonelik = models.ForeignKey('HaftalikPlanModel', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="abonelik_parahareketi_relations")
    etkinlik = models.ForeignKey('EtkinlikModel', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="etkinlik_parahareketi_relations")
    aciklama = models.CharField('Açıklama', max_length=250, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name="user_parahareketi_relations", null=True, blank=True)

    def __str__(self):
        return str(self.uye) + " " + str(self.tutar) + " " + str(self.tarih)

    class Meta:
        verbose_name = "Para Hareketleri"
        verbose_name_plural = "Para Hareketleri"
        ordering = ["id"]

    # def save(self, *args, **kwargs):


class UcretTarifesiModel(BaseAbstract):
    adi = models.CharField(max_length=50, verbose_name="Adı", null=False, blank=False)
    seviye = models.CharField(max_length=20, choices=SeviyeEnum.choices(), null=False, blank=False)
    abonelik_tipi = models.CharField(max_length=20, choices=AbonelikTipiEnum.ucret_tarifesinde_kullanilacaklar(), null=False, blank=False)
    kisi_sayisi = models.SmallIntegerField(verbose_name="Kişi Sayısı", null=False, blank=False)
    kisi_basi_ucret = models.SmallIntegerField(verbose_name="Kişi Başı Ücret", null=False, blank=False)
    ders_sayisi = models.SmallIntegerField(verbose_name="Ders Sayısı", null=True, blank=True)

    def __str__(self):
        return self.adi

    def toplam_ucret(self):
        return self.kisi_basi_ucret * self.kisi_sayisi
