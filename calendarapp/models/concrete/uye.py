from django.db import models
from django.db.models.signals import post_save, post_delete

from accounts.models import User
from calendarapp.models.abstract.base_abstract import BaseAbstract


class UyeManager(models.Manager):

    def getir_butun_uyelerler(self, user=None):
        events = UyeModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events


class UyeModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=False, blank=False)
    soyadi = models.CharField('Soyadı', max_length=250, null=False, blank=False)
    kimlikNo = models.CharField("KimlikNo", max_length=11, blank=True, null=True)
    telefon = models.CharField('Telefon', max_length=11, null=True, blank=True)
    email = models.EmailField('E-Mail', max_length=250, null=True, blank=True)
    adres = models.TextField('Adres', max_length=250, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="uye", null=True, blank=True,
                             verbose_name="Ekleyen")

    # il = models.ForeignKey(SehirModel, on_delete=models.SET_NULL, null=True, blank=True,
    #                        related_name='musterinin_sehri', verbose_name='Şehir')
    # ilce = models.ForeignKey(IlceModel, on_delete=models.SET_NULL, null=True, blank=True,
    #                          related_name='musterinin_ilcesi', verbose_name='İlçe')
    # sube = models.ForeignKey(SubeModel, on_delete=models.SET_NULL, null=True, blank=True,
    #                          related_name='musterinin_subesi', verbose_name='Şube')
    # aktifMi = models.BooleanField('Aktif Mi', null=False, blank=False, default=True)
    # tipi = models.ForeignKey(MusteriTipiModel, on_delete=models.SET_NULL, null=True, blank=True,
    #                          related_name='musterinin_tipi', verbose_name='Müşteri Tipi')

    def __str__(self):
        return str(self.adi) + " " + str(self.soyadi)

    objects = UyeManager()

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ["-id"]

    def delete(self, *args, **kwargs):
        UyeGrupModel.objects.filter(uye1=self, uye2__isnull=True, uye3__isnull=True, uye4__isnull=True).delete()
        super(UyeModel, self).delete(*args, **kwargs)


class UyeGrupModel(BaseAbstract):
    uye1 = models.ForeignKey(UyeModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="uye1")
    uye2 = models.ForeignKey(UyeModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="uye2")
    uye3 = models.ForeignKey(UyeModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="uye3")
    uye4 = models.ForeignKey(UyeModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="uye4")

    def __str__(self):
        value = ""
        if self.uye1:
            value += " 1-" + str(self.uye1)
        if self.uye2:
            value += " 2-" + str(self.uye2)
        if self.uye3:
            value += " 3-" + str(self.uye3)
        if self.uye4:
            value += " 4-" + str(self.uye4)
        return value

    class Meta:
        verbose_name = "Üye Grubu"
        verbose_name_plural = "Gruplar"
        ordering = ["-id"]


def grup_kaydi_olustur(sender, instance, **kwargs):
    if not UyeGrupModel.objects.filter(uye1=instance).exists():
        UyeGrupModel.objects.create(uye1=instance)


def grup_kaydi_sil(sender, instance, **kwargs):
    uye = UyeGrupModel.objects.filter(uye1_id=instance.id)
    print(instance.id)
    print(uye)
    if uye.exists():
        uye.delete()


post_save.connect(grup_kaydi_olustur, sender=UyeModel)
