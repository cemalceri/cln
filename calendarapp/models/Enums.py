from datetime import datetime
from enum import Enum, IntEnum

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


class UyeTipiEnum(IntEnum):
    Yetişkin = 1
    Sporcu = 2

    @classmethod
    def choices(cls):
        return [(key.name, key.value,) for key in cls]


class AntrenorRenkEnum(Enum):
    red = "Kırmızı"
    orange = "Turuncu"
    yellow = "Sarı"

    @classmethod
    def choices(cls):
        return [(key.name, key.value,) for key in cls]


class CinsiyetEnum(Enum):
    Erkek = "Erkek"
    Kadın = "Kadın"

    @classmethod
    def choices(cls):
        return [(key.name, key.value,) for key in cls]


class AbonelikTipiEnum(Enum):
    Uyelik = "Üyelik"
    Paket = "Paket"
    Telafi = "Telafi"
    Demo = "Demo"
    TekDers = "Tek Ders"
    Diger = "Diğer"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def etkinlik_kaydinda_kullanilacaklar(cls):
        return [(key.name, key.value) for key in cls if key.name in ["Telafi", "Demo", "TekDers", "Diger"]]

    @classmethod
    def haftalik_plan_kaydinda_kullanilacaklar(cls):
        return [(key.name, key.value) for key in cls if key.name in ["Uyelik", "Paket"]]

    @classmethod
    def ucret_tarifesinde_kullanilacaklar(cls):
        return [(key.name, key.value) for key in cls if key.name in ["Uyelik", "Paket", "Demo", "TekDers"]]


class ParaHareketTuruEnum(Enum):
    Borc = "Borç"
    Odeme = "Ödeme"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


class UcretTuruEnum(Enum):
    Aidat = "Aidat"
    Paket = "Paket"
    TekDers = "Tek Ders"
    FarkUcreti = "Fark Ücreti"
    Diger = "Diğer"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


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
