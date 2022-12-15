# Generated by Django 3.2.13 on 2022-12-12 23:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0027_auto_20221212_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='haftalikplanmodel',
            name='baslangic_tarih_saat',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Başlangıç Tarih Saat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='haftalikplanmodel',
            name='bitis_tarih_saat',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Bitiş Tarih Saat'),
            preserve_default=False,
        ),
    ]