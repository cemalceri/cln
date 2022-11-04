from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete

from django.conf import settings
from calendarapp.models.Enums import SeviyeRenkEnum, GrupOdemeSekliEnum
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
    seviye_rengi = models.CharField(max_length=20, choices=SeviyeRenkEnum.choices(), default="red",
                                    verbose_name="Seviye Rengi")
    okul = models.ForeignKey('OkulModel', on_delete=models.SET_NULL, related_name="okul", null=True, blank=True)
    onaylandi_mi = models.BooleanField('Onay Durumu', default=False)
    aktif_mi = models.BooleanField('Aktif mi', default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="uye", null=True, blank=True,
                             verbose_name="Ekleyen")

    def __str__(self):
        return str(self.adi) + " " + str(self.soyadi)

    objects = UyeManager()

    def delete(self, *args, **kwargs):
        # ilk kayıtta kendi için oluşturulan grubun silinmesi
        grup_ids = UyeGrupModel.objects.filter(uye_id=self.id).values_list('grup_id', flat=True)
        GrupModel.objects.filter(id__in=grup_ids, tekil_mi=True).delete()
        # Grupta son kalan kişiyse grup silinir
        for id in grup_ids:
            if UyeGrupModel.objects.filter(grup_id=id).count() == 1:
                GrupModel.objects.filter(id=id).delete()
        super(UyeModel, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ["-id"]


class GrupModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=True, blank=True)
    tekil_mi = models.BooleanField('Tekil Mi', default=False)

    class Meta:
        verbose_name = "Gruplar"
        verbose_name_plural = "Gruplar"
        ordering = ["-id"]

    def __str__(self):
        if self.tekil_mi is True:
            return str(self.grup_uyegrup_relations.first().uye.uye_no) \
                   + "-" + self.grup_uyegrup_relations.first().uye.adi + " " + self.grup_uyegrup_relations.first().uye.soyadi
        else:
            if self.adi is None or self.adi == "":
                string = ""
                grup = UyeGrupModel.objects.filter(grup_id=self.id)
                string += "( " + str(grup.count()) + " Üyeli Grup) "
                for item in grup:
                    string += str(item.uye.uye_no) + "-" + item.uye.adi + " " + item.uye.soyadi + " / "
                return string
            else:
                return self.adi


def renk(self):
    return UyeGrupModel.objects.filter(grup_id=self.id).first().uye.seviye_rengi


class UyeGrupModel(BaseAbstract):
    grup = models.ForeignKey(GrupModel, on_delete=models.CASCADE, related_name="grup_uyegrup_relations", null=False,
                             blank=False)
    uye = models.ForeignKey(UyeModel, on_delete=models.CASCADE, null=False, blank=False,
                            related_name="uye_uyegrup_relations")
    odeme_sekli = models.SmallIntegerField('Ödeme Şekli', choices=GrupOdemeSekliEnum.choices(), null=True, blank=True)

    def __str__(self):
        return self.uye.adi + " " + self.uye.soyadi

    class Meta:
        verbose_name = "Üye Grubu"
        verbose_name_plural = "Üye Gruplar"
        ordering = ["-id"]

    def delete(self, *args, **kwargs):
        # grupta son kalan kişi ise grup silinir
        if UyeGrupModel.objects.filter(grup_id=self.grup.id).count() == 1:
            GrupModel.objects.filter(pk=self.grup.id).delete()
        super(UyeGrupModel, self).delete(*args, **kwargs)


def grup_kaydi_olustur(sender, instance, **kwargs):
    # Daha önce UyeGrup tablosunda kendisi için kayıt oluşturulmadıysa
    if not UyeGrupModel.objects.filter(uye=instance, grup__tekil_mi=True):
        grup = GrupModel.objects.create(tekil_mi=True,
                                        adi=str(instance.uye_no) + " - " + instance.adi + " " + instance.soyadi)
        UyeGrupModel.objects.create(uye=instance, grup=grup)


post_save.connect(grup_kaydi_olustur, sender=UyeModel)
