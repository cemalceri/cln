from enum import Enum


class RenkEnum(Enum):
    Kırmızı = "red"
    Mavi = "blue"
    Sarı = "yellow"
    Yeşil = "green"


    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
