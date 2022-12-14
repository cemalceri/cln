from django.conf import settings
from django.db import models

from calendarapp.models.Enums import AbonelikTipiEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeModel, GrupModel


class UyeAbonelikModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    grup = models.ForeignKey(GrupModel, verbose_name="Katılımcı Grubu", on_delete=models.CASCADE, blank=False,
                             null=False)
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

    @property
    def dakika_degeri(self):
        return self.bitis_tarih_saat - self.baslangic_tarih_saat


class UyePaketModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    grup_mu = models.BooleanField("Grup Paketi Mi?", default=False, blank=False, null=False)
    baslangic_tarih = models.DateField("Başlangıç Tarihi", null=False, blank=False)
    bitis_tarih = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)
    adet = models.IntegerField(verbose_name="Adet", null=False, blank=False)
    toplam_fiyati = models.IntegerField(verbose_name="Toplam Fiyatı", null=False, blank=False)
    ozellikler = models.TextField(max_length=500, verbose_name="Özellikler", null=True, blank=True)
    aktif_mi = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name="uyepaket_relations", null=True, blank=True, verbose_name="Ekleyen")

    def kalan_adet(self):
        kullanilan_adet = PaketKullanimModel.objects.filter(uye_paket_id=self.id).count()
        return self.adet - kullanilan_adet

    class Meta:
        verbose_name = "Üyenin Paketleri"
        verbose_name_plural = "Üyenin Paketleri"
        ordering = ["id"]

    def __str__(self):
        return str(self.uye) + "-" + str(self.kort) + " - Adet: " + str(self.adet)


class PaketKullanimModel(BaseAbstract):
    uye_paket = models.ForeignKey(UyePaketModel, verbose_name="Paket", on_delete=models.CASCADE, blank=False,
                                  null=False)
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    etkinlik = models.ForeignKey(EtkinlikModel, verbose_name="Etkinlik", on_delete=models.CASCADE, blank=False,
                                 null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="paket_kullanim",
                             null=True, blank=True, verbose_name="Ekleyen")

    def __str__(self):
        return str(self.etkinlik) + " " + str(self.uye)

    class Meta:
        verbose_name = "Paket Kullanım"
        verbose_name_plural = "Paket Kullanım"
        ordering = ["id"]

    # def save(self, *args, **kwargs):
    #     # Paketin sonu ise aktif false yapılır
    #     self.kalan_adet = self.abonelik.kalan_adet() - 1
    #     if self.abonelik.paket.tipi == AbonelikTipikEnum.Paket.value and self.abonelik.kalan_adet() <= 1:
    #         self.abonelik.aktif_mi = False
    #         self.abonelik.save()
    #     super(PaketKullanimModel, self).save(*args, **kwargs)
