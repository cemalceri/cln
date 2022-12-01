from django.conf import settings
from django.db import models

from calendarapp.models.Enums import AbonelikTipiEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeModel, GrupModel


class UyeAbonelikModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    grup = models.ForeignKey(GrupModel, verbose_name="Katılımcı Grubu", on_delete=models.CASCADE, blank=False, null=False)
    kort = models.ForeignKey(KortModel, verbose_name="Kort", on_delete=models.CASCADE, blank=False, null=False)
    haftanin_gunu = models.IntegerField(verbose_name="Gün", blank=True, null=True)
    gun_adi = models.CharField(max_length=20, verbose_name="Gün Adı", blank=False, null=False)
    baslangic_tarih_saat = models.DateTimeField("Başlangıç Tarihi", null=False, blank=False)
    bitis_tarih_saat = models.DateTimeField(verbose_name="Bitiş Tarihi", null=False, blank=False)
    aktif_mi = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="abonelik", null=True,
                             blank=True, verbose_name="Ekleyen")

    def __str__(self):
        return self.uye.adi + " " + self.uye.soyadi + " " + self.gun_adi
        #    + " - Başlangıç: " \
        #    + self.baslangic_tarihi.strftime(
        # "%d-%m-%Y") + " - Bitiş: " + self.bitis_tarihi.strftime("%d-%m-%Y")

    class Meta:
        verbose_name = "Abonelik"
        verbose_name_plural = "Abonelik"
        ordering = ["id"]

    # def kalan_adet(self):
    #     if self.paket.tipi is AbonelikTipiEnum.Paket.value and self.paket.adet is not None:
    #         kullanim_sayisi = PaketKullanimModel.objects.filter(abonelik=self).count()
    #         return self.paket.adet - kullanim_sayisi
    #     return None
    #
    # def son_yapilan_odeme_tarihi(self):
    #     son_odeme = self.paket.paket_parahareketi_relations.filter().order_by("-tarih").first()
    #     if son_odeme:
    #         return son_odeme.tarih
    #     return None
    #
    # def son_yapilan_odeme_tutari(self):
    #     son_odeme = self.paket.paket_parahareketi_relations.filter().order_by("-tarih").first()
    #     if son_odeme:
    #         return son_odeme.tutar
    #     return None

    @property
    def dakika_degeri(self):
        return self.bitis_tarih_saat - self.baslangic_tarih_saat


class PaketModel(BaseAbstract):
    adi = models.CharField(max_length=200, verbose_name="Paket / Abonelik Adı")
    tipi = models.SmallIntegerField(verbose_name="Tipi", choices=AbonelikTipiEnum.choices(), blank=False, null=False,
                                    default=AbonelikTipiEnum.Üyelik)
    adet = models.IntegerField(verbose_name="Adet", null=True, blank=True)
    toplam_fiyati = models.IntegerField(verbose_name="Toplam Fiyatı", null=True, blank=True)
    ozellikler = models.TextField(max_length=500, verbose_name="Özellikler", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="paket", null=True,
                             blank=True, verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Paket ve Abonelik Çeşitleri"
        verbose_name_plural = "Paket ve Abonelik Çeşitleri"
        ordering = ["id"]


class PaketKullanimModel(BaseAbstract):
    abonelik = models.ForeignKey(UyeAbonelikModel, verbose_name="Abonelik", on_delete=models.CASCADE, blank=False,
                                 null=False)
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    etkinlik = models.ForeignKey(EtkinlikModel, verbose_name="Etkinlik", on_delete=models.CASCADE, blank=False,
                                 null=False)
    kalan_adet = models.SmallIntegerField(verbose_name="Kalan Adet", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="paket_kullanim",
                             null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return str(self.abonelik) + " " + str(self.uye)

    class Meta:
        verbose_name = "Paket Kullanım"
        verbose_name_plural = "Paket Kullanım"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        # Paketin sonu ise aktif false yapılır
        self.kalan_adet = self.abonelik.kalan_adet() - 1
        if self.abonelik.paket.tipi == AbonelikTipikEnum.Paket.value and self.abonelik.kalan_adet() <= 1:
            self.abonelik.aktif_mi = False
            self.abonelik.save()
        super(PaketKullanimModel, self).save(*args, **kwargs)
