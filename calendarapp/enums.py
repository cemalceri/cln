from enum import IntEnum, Enum
from django.db import models


# Area
class CinsiyetEnum(IntEnum):
    Erkek = 1
    Kadın = 2
    __labels__ = {
        Erkek: "Erkek",
        Kadın: "Kadın",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AktifPasifEnum(IntEnum):
    Aktif = 1
    Pasif = 0
    __labels__ = {
        Aktif: "Aktif",
        Pasif: "Pasif",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class SehirlerEnum(IntEnum):
    Ankara = 6
    Eskisehir = 26
    __labels__ = {
        Ankara: "Ankara",
        Eskisehir: "Eskişehir",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class IlcelerEnum(IntEnum):
    Odunpazari = 1
    Tepebasi = 2
    kecioren = 3
    __labels__ = {
        Odunpazari: "Odunpazarı",
        Tepebasi: "Tepebaşı",
        kecioren: "Keçiören",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Birimler(IntEnum):
    TL = 1
    Kg = 2
    Adet = 3
    Koli = 4
    Çuval = 5
    Paket = 6
    __labels__ = {
        TL: "TL",
        Kg: "Kg",
        Adet: "Adet",
        Koli: "Koli",
        Çuval: "Çuval",
        Paket: "Paket",
    }

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class DosyaKaynakEnum(IntEnum):
    Vatandaş = 1
    Yardım= 2
    Dağıtım = 3
    Bağış = 4
    __labels__ = {
        Vatandaş: "Vatandaş",
        Yardım: "Yardım",
        Dağıtım: "Dağıtım",
        Bağış: "Bağış",
    }

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