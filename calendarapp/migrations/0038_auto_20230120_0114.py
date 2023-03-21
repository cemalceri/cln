# Generated by Django 3.2.13 on 2023-01-20 01:14

import calendarapp.models.Enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0037_auto_20230118_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etkinlikmodel',
            name='abonelik_tipi',
            field=models.CharField(choices=[('Telafi', 'Telafi'), ('Demo', 'Demo'), ('TekDers', 'Tek Ders'), ('Diger', 'Diğer')], default=calendarapp.models.Enums.AbonelikTipiEnum['TekDers'], max_length=20, verbose_name='Ders Tipi'),
        ),
        migrations.AlterField(
            model_name='haftalikplanmodel',
            name='abonelik_tipi',
            field=models.CharField(choices=[('Paket', 'Paket'), ('Aidat', 'Aidat')], default=calendarapp.models.Enums.AbonelikTipiEnum['Aidat'], max_length=50, verbose_name='Abonelik Tipi'),
        ),
    ]
