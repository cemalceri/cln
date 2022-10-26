from django.db import models

from accounts.models import User
from calendarapp.models.Enums import AbonelikTipikEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.uye import UyeModel


class AbonelikModel(BaseAbstract):
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    paket = models.ForeignKey("PaketModel", verbose_name="Paket", on_delete=models.PROTECT, blank=False, null=False)
    baslangic_tarihi = models.DateField(verbose_name="Başlangıç Tarihi", null=False, blank=False)
    bitis_tarihi = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)
    aktif_mi = models.BooleanField(default=True)
    aciklama = models.TextField(verbose_name="Açıklama", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="abonelik", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.paket.adi
        #    + " - Başlangıç: " \
        #    + self.baslangic_tarihi.strftime(
        # "%d-%m-%Y") + " - Bitiş: " + self.bitis_tarihi.strftime("%d-%m-%Y")

    class Meta:
        verbose_name = "Abonelik"
        verbose_name_plural = "Abonelik"
        ordering = ["id"]

    def kalan_adet(self):
        if self.paket.tipi is AbonelikTipikEnum.Paket.value and self.paket.adet is not None:
            kullanim_sayisi = PaketKullanimModel.objects.filter(abonelik=self).count()
            return self.paket.adet - kullanim_sayisi
        return None

    def son_yapilan_odeme_tarihi(self):
        son_odeme = self.paket.paket_parahareketi_relations.filter().order_by("-tarih").first()
        if son_odeme:
            return son_odeme.tarih
        return None

    def son_yapilan_odeme_tutari(self):
        son_odeme = self.paket.paket_parahareketi_relations.filter().order_by("-tarih").first()
        if son_odeme:
            return son_odeme.tutar
        return None


class PaketModel(BaseAbstract):
    adi = models.CharField(max_length=200, verbose_name="Paket Adı")
    tipi = models.SmallIntegerField(verbose_name="Tipi", choices=AbonelikTipikEnum.choices(), blank=False, null=False,
                                    default=AbonelikTipikEnum.Uyelik)
    adet = models.IntegerField(verbose_name="Adet", null=True, blank=True)
    toplam_fiyati = models.IntegerField(verbose_name="Toplam Fiyatı", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="paket", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return self.adi

    class Meta:
        verbose_name = "Paket ve Abonelik Çeşitleri"
        verbose_name_plural = "Paket ve Abonelik Çeşitleri"
        ordering = ["id"]


class PaketKullanimModel(BaseAbstract):
    abonelik = models.ForeignKey(AbonelikModel, verbose_name="Abonelik", on_delete=models.CASCADE, blank=False,
                                 null=False)
    uye = models.ForeignKey(UyeModel, verbose_name="Üye", on_delete=models.CASCADE, blank=False, null=False)
    etkinlik = models.ForeignKey(EtkinlikModel, verbose_name="Etkinlik", on_delete=models.CASCADE, blank=False,
                                 null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="paket_kullanim", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return str(self.abonelik) + " " + self.uye.adi + " " + self.uye.soyadi

    class Meta:
        verbose_name = "Paket Kullanım"
        verbose_name_plural = "Paket Kullanım"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        # Paketin sonu ise aktif false yapılır
        print(self.abonelik.kalan_adet())
        if self.abonelik.paket.tipi == AbonelikTipikEnum.Paket.value and self.abonelik.kalan_adet() >= 1:
            self.abonelik.aktif_mi = False
            self.abonelik.save()
        super(PaketKullanimModel, self).save(*args, **kwargs)
