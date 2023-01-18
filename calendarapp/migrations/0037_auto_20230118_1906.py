# Generated by Django 3.2.3 on 2023-01-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0036_auto_20230118_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etkinlikmodel',
            name='abonelik_tipi',
            field=models.IntegerField(choices=[('Telafi', 'Telafi'), ('Demo', 'Demo'), ('TekDers', 'Tek Ders'), ('Diger', 'Diğer')], default=2, verbose_name='Ders Tipi'),
        ),
        migrations.AlterField(
            model_name='haftalikplanmodel',
            name='abonelik_tipi',
            field=models.IntegerField(choices=[('Paket', 'Paket')], default=2, verbose_name='Abonelik Tipi'),
        ),
    ]