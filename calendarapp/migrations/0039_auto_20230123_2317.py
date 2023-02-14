# Generated by Django 3.2.13 on 2023-01-23 23:17

import calendarapp.models.Enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0038_auto_20230120_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antrenormodel',
            name='renk',
            field=models.CharField(choices=[('red', 'Kırmızı'), ('orange', 'Turuncu'), ('yellow', 'Sarı')], default='gray', max_length=20, verbose_name='Renk'),
        ),
        migrations.AlterField(
            model_name='haftalikplanmodel',
            name='abonelik_tipi',
            field=models.CharField(choices=[('Uyelik', 'Üyelik'), ('Paket', 'Paket')], default=calendarapp.models.Enums.AbonelikTipiEnum['Uyelik'], max_length=50, verbose_name='Abonelik Tipi'),
        ),
    ]