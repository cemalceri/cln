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


def uye_no_uret():
    try:
        last = UyeModel.objects.all().order_by('uye_no').last()
        if not last:
            return 100
        return last.uye_no + 1
    except:
        return 100


class UyeModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=False, blank=False)
    soyadi = models.CharField('Soyadı', max_length=250, null=False, blank=False)
    dogum_tarihi = models.DateField('Doğum Tarihi', null=True, blank=True)
    uye_no = models.IntegerField('Üye No', default=uye_no_uret, null=False, blank=False)
    kimlikNo = models.CharField("KimlikNo", max_length=11, blank=True, null=True)
    telefon = models.CharField('Telefon', max_length=11, null=True, blank=True)
    email = models.EmailField('E-Mail', max_length=250, null=True, blank=True)
    adres = models.TextField('Adres', max_length=250, null=True, blank=True)
    onaylandi_mi = models.BooleanField('Onaylandı mı', default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="uye", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return str(self.adi) + " " + str(self.soyadi)

    objects = UyeManager()

    def delete(self, *args, **kwargs):
        uye_grup = UyeGrupModel.objects.filter(uye_id=self.id)
        GrupModel.objects.filter(pk=uye_grup.first().grup_id, tekil_mi=True).delete()
        super(UyeModel, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ["-id"]


class GrupModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=True, blank=False)
    tekil_mi = models.BooleanField('Tekil Mi', default=False)

    class Meta:
        verbose_name = "Gruplar"
        verbose_name_plural = "Gruplar"
        ordering = ["-id"]

    def __str__(self):
        if self.tekil_mi is True:
            return str(self.adi)
        else:
            string = ""
            for item in UyeGrupModel.objects.filter(grup_id=self.id):
                string += item.uye.adi + " " + item.uye.soyadi + " - "
            return string


class UyeGrupModel(BaseAbstract):
    grup = models.ForeignKey(GrupModel, on_delete=models.CASCADE, related_name="grup_uyegrup_relations", null=False,
                             blank=False)
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, null=False, blank=False,
                            related_name="uye_uyegrup_relations")
    odeme_sekli = models.CharField('Ödeme Şekli', max_length=250, null=True, blank=True)

    def __str__(self):
        return self.uye.adi + " " + self.uye.soyadi

    class Meta:
        verbose_name = "Üye Grubu"
        verbose_name_plural = "Üye Gruplar"
        ordering = ["-id"]


def grup_kaydi_olustur(sender, instance, **kwargs):
    UyeGrupModel.objects.create(uye=instance, grup=GrupModel.objects.create(tekil_mi=True,
                                                                            adi=instance.adi + " " + instance.soyadi))


post_save.connect(grup_kaydi_olustur, sender=UyeModel)
