# Generated by Django 3.2.3 on 2022-10-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0004_auto_20221025_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='paketkullanimmodel',
            name='kalan_adet',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Kalan Adet'),
        ),
    ]
