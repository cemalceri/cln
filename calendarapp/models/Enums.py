from datetime import datetime
from enum import Enum

from django.db import models


class SeviyeEnum(Enum):
    Kirmizi = "Kırmızı"
    Turuncu = "Turuncu"
    Sari = "Sarı"
    Yesil = "Yeşil"
    Yetiskin = "Yetişkin"
    TenisOkulu = "Tenis Okulu"

    @classmethod
    def choices(cls):
        return [(key.name, key.value,) for key in cls]


class GunlerModel(models.Model):
    adi = models.CharField(max_length=250, null=False, blank=False)
    haftanin_gunu = models.IntegerField(verbose_name="Haftanın Kaçıncı Günü", null=False, blank=False)
    hafta_ici_mi = models.BooleanField(verbose_name="Hafta için mi", default=False)

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Günler"
        verbose_name_plural = "Günler"
        ordering = ["id"]


class SaatlerModel(models.Model):
    adi = models.CharField(max_length=250, null=False, blank=False)
    baslangic_degeri = models.TimeField(null=False, blank=False)
    bitis_degeri = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Saatler"
        verbose_name_plural = "Saatler"
        ordering = ["id"]


class AbonelikTipiEnum(Enum):
    Paket = "Paket"
    Uyelik = "Üyelik"
    Telafi = "Telafi"
    Demo = "Demo"
    TekDers = "Tek Ders"
    Diger = "Diğer"

    @classmethod
    def choices(cls):
        return [(key.name,key.value) for key in cls]

    @classmethod
    def etkinlik_kaydinda_kullanilacaklar(cls):
        return [(key.name, key.value ) for key in cls if key.name in ["Telafi", "Demo", "TekDers", "Diger"]]

    @classmethod
    def haftalik_plan_kaydinda_kullanilacaklar(cls):
        return [(key.name, key.value) for key in cls if key.name in ["Paket", "Uyelik"]]


class ParaHareketTuruEnum(Enum):
    Giris = 1
    Cikis = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class OdemeTuruEnum(Enum):
    Maaş = 1
    Yol = 2
    Yemek = 3
    Diğer = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class GrupOdemeSekliEnum(Enum):
    Ortak_Odeme = 1
    Bireysel_Odeme = 2
    __labels__ = {
        Ortak_Odeme: "Ortak Ödeme",
        Bireysel_Odeme: "Bireysel Ödeme",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class KatilimDurumuEnum(Enum):
    Katıldı = 1
    Katılmadı = 2
    İptal = 3
    __labels__ = {
        Katıldı: "Katıldı",
        Katılmadı: "Katılmadı",
        İptal: "İptal",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class GunEnum:
    Pazartesi = 1
    Salı = 2
    Çarşamba = 3
    Perşembe = 4
    Cuma = 5
    Cumartesi = 6
    Pazar = 7
    __labels__ = {
        Pazartesi: "Pazartesi",
        Salı: "Salı",
        Çarşamba: "Çarşamba",
        Perşembe: "Perşembe",
        Cuma: "Cuma",
        Cumartesi: "Cumartesi",
        Pazar: "Pazar",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
