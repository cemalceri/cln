from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete

from django.conf import settings
from calendarapp.models.Enums import SeviyeEnum, GrupOdemeSekliEnum, UyeTipiEnum, CinsiyetEnum
from calendarapp.models.abstract.base_abstract import BaseAbstract
from calendarapp.models.concrete.commons import GunlerModel, SaatlerModel, OkulModel


class UyeManager(models.Manager):

    def getir_butun_uyelerler(self, user=None):
        events = UyeModel.objects.filter(
            # user=user,
            is_active=True, is_deleted=False)
        return events


def uye_no_uret():
    any = UyeModel.objects.order_by('-uye_no').first()
    if any:
        return any.uye_no + 1
    return 100


class UyeModel(BaseAbstract):
    # Ortak alanlar
    adi = models.CharField('Adı', max_length=30, null=False, blank=False)
    soyadi = models.CharField('Soyadı', max_length=30, null=False, blank=False)
    kimlik_no = models.CharField("Kimlik No", max_length=11, blank=True, null=True)
    cinsiyet = models.CharField('Cinsiyet', max_length=10, choices=CinsiyetEnum.choices(), null=True, blank=True)
    telefon = models.CharField('Telefon', max_length=11, null=True, blank=True)
    email = models.EmailField('E-Mail', max_length=50, null=True, blank=True)
    dogum_tarihi = models.DateField('Doğum Tarihi', null=True, blank=True)
    dogum_yeri = models.CharField('Doğum Yeri', max_length=50, null=True, blank=True)
    adres = models.CharField('Adres', max_length=250, null=True, blank=True)
    uye_no = models.IntegerField('Üye No', default=uye_no_uret, null=False, blank=False)
    seviye_rengi = models.CharField("Seviye Rengi", max_length=20, choices=SeviyeEnum.choices(), default="red")
    onaylandi_mi = models.BooleanField('Onay Durumu', null=True, blank=True, default=False)
    aktif_mi = models.BooleanField('Aktif mi', null=True, blank=True, default=True)
    uye_tipi = models.SmallIntegerField('Üye Tipi', choices=UyeTipiEnum.choices(), default=UyeTipiEnum.Yetişkin.value,
                                        null=False, blank=False)
    referansi = models.CharField('Referans', max_length=50, null=True, blank=True)
    tenis_gecmisi_var_mi = models.CharField('Tenis Eğitim Geçmişi',
                                            choices=[('Var', 'Var'), ('Yok', 'Yok'), ('Az', 'Az')],
                                            max_length=10, null=True, blank=True)
    program_tercihi = models.CharField('Program Tercihi', max_length=100, null=True, blank=True,
                                       choices=[('Özel Ders', 'Özel Ders'), ('Grup', 'Grup'), ('Hobi', 'Hobi'),
                                                ('Altyapı', 'Altyapı')])
    gunler = models.ManyToManyField(GunlerModel, verbose_name='Tercih Edilen Günler', blank=True, null=True,
                                    related_name='gunler_uye_tablosu')
    saatler = models.ManyToManyField(SaatlerModel, verbose_name='Tercih Edilen Saatler', blank=True, null=True,
                                     related_name='saatler_uye_tablosu')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="uye", null=True,
                             blank=True, verbose_name="Ekleyen")
    # Yetişkin
    meslek = models.CharField('Meslek', max_length=50, null=True, blank=True)

    # Genç
    anne_adi_soyadi = models.CharField('Anne Ad Soyad', max_length=30, null=True, blank=True)
    anne_telefon = models.CharField('Anne Telefon', max_length=11, null=True, blank=True)
    anne_mail = models.EmailField('Anne E-Mail', max_length=50, null=True, blank=True)
    anne_meslek = models.CharField('Anne Meslek', max_length=50, null=True, blank=True)
    baba_adi_soyadi = models.CharField('Baba Ad Soyad', max_length=30, null=True, blank=True)
    baba_telefon = models.CharField('Baba Telefon', max_length=11, null=True, blank=True)
    baba_mail = models.EmailField('Baba E-Mail', max_length=50, null=True, blank=True)
    baba_meslek = models.CharField('Baba Meslek', max_length=50, null=True, blank=True)
    okul = models.ForeignKey(OkulModel, on_delete=models.SET_NULL, related_name="okul", null=True, blank=True)

    def __str__(self):
        return str(self.adi) + " " + str(self.soyadi) + " (" + str(self.uye_no) + ")"

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

    def tercih_edilen_gunler(self):
        return " / ".join([str(i) for i in self.gunler.all()])

    def tercih_edilen_saatler(self):
        return " / ".join([str(i) for i in self.saatler.all()])


class GrupModel(BaseAbstract):
    adi = models.CharField('Adı', max_length=250, null=True, blank=True)
    tekil_mi = models.BooleanField('Tekil Mi', default=False)

    class Meta:
        verbose_name = "Gruplar"
        verbose_name_plural = "Gruplar"
        ordering = ["-id"]

    def __str__(self):
        if self.tekil_mi is True:
            return self.grup_uyegrup_relations.first().uye.adi + " " + self.grup_uyegrup_relations.first().uye.soyadi + " (" + str(
                self.grup_uyegrup_relations.first().uye.uye_no) + ")"
        else:
            if self.adi is None or self.adi == "":
                string = ""
                grup = UyeGrupModel.objects.filter(grup_id=self.id)
                string += "|" + str(grup.count()) + " Üyeli Grup| "
                for item in grup:
                    string += item.uye.adi + " " + item.uye.soyadi + " (" + str(item.uye.uye_no) + ") -"
                return string[:-1]
            else:
                return self.adi

    def renk(self):
        return UyeGrupModel.objects.filter(grup_id=self.id).first().uye.seviye_rengi

    def uye_sayisi(self):
        return len(UyeGrupModel.objects.filter(grup_id=self.id))


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
