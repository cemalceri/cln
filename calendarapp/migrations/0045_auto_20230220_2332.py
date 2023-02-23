# Generated by Django 3.2.13 on 2023-02-20 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0044_auto_20230217_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uyemodel',
            name='veli_adi_soyadi',
        ),
        migrations.RemoveField(
            model_name='uyemodel',
            name='veli_telefon',
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='anne_adi_soyadi',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Anne Ad Soyad'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='anne_mail',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='Anne E-Mail'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='anne_meslek',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Anne Meslek'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='anne_telefon',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Anne Telefon'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='baba_adi_soyadi',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Baba Ad Soyad'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='baba_mail',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='Baba E-Mail'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='baba_meslek',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Baba Meslek'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='baba_telefon',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Baba Telefon'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='cinsiyet',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Cinsiyet'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='dogum_yeri',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Doğum Yeri'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='gunler',
            field=models.ManyToManyField(blank=True, null=True, related_name='gunler_uye_tablosu', to='calendarapp.GunlerModel', verbose_name='Tercih Edilen Günler'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='meslek',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Meslek'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='program_tercihi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Program Tercihi'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='referansi',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Referans'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='saatler',
            field=models.ManyToManyField(blank=True, null=True, related_name='saatler_uye_tablosu', to='calendarapp.SaatlerModel', verbose_name='Tercih Edilen Saatler'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='tenis_gecmisi_var_mi',
            field=models.BooleanField(blank=True, null=True, verbose_name='Tenis Eğitim Geçmişi'),
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='adi',
            field=models.CharField(max_length=30, verbose_name='Adı'),
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='soyadi',
            field=models.CharField(max_length=30, verbose_name='Soyadı'),
        ),
    ]