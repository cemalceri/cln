from django.apps import AppConfig


class CalendarappConfig(AppConfig):
    name = "calendarapp"

    def ready(self):
        saatler_yoksa_ekle()
        gunler_yoksa_ekle()


def saatler_yoksa_ekle():
    from calendarapp.models.Enums import SaatlerModel
    if SaatlerModel.objects.count() == 0:
        from datetime import datetime
        from datetime import timedelta
        baslangic_degeri = datetime(1970, 1, 1, 00, 00, 00)
        bitis_degeri = datetime(1970, 1, 1, 00, 30, 00)
        i = 0
        for i in range(0, 48):
            SaatlerModel.objects.create(adi=str(baslangic_degeri.time()) + " - " + str(bitis_degeri.time()),
                                        baslangic_degeri=baslangic_degeri, bitis_degeri=bitis_degeri)
            baslangic_degeri += timedelta(minutes=30)
            bitis_degeri += timedelta(minutes=30)


def gunler_yoksa_ekle():
    from calendarapp.models.Enums import GunlerModel
    if GunlerModel.objects.count() == 0:
        GunlerModel.objects.create(adi="Pazartesi", haftanin_gunu=1, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Salı", haftanin_gunu=2, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Çarşamba", haftanin_gunu=3, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Perşembe", haftanin_gunu=4, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Cuma", haftanin_gunu=5, hafta_ici_mi=True)
        GunlerModel.objects.create(adi="Cumartesi", haftanin_gunu=6, hafta_ici_mi=False)
        GunlerModel.objects.create(adi="Pazar", haftanin_gunu=7, hafta_ici_mi=False)

